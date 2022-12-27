from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.common.views import ExtendedViewSet
from apps.temp_mail.helpers import TempMailHelper
from apps.temp_mail.models import TempMail, Message
from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping
from apps.temp_mail.serializers import TempMailSerializer, DomainSerializer, TempMailMessageSerializer


class TempMailViewSet(
    ExtendedViewSet
):
    queryset = TempMail.objects.all()
    serializer_class = TempMailSerializer
    permission_classes = [AllowAny]

    @action(methods=['get'], detail=False, url_path='get_all_domains', serializer_class=DomainSerializer)
    def get_all_domains(self, request, *args, **kwargs):
        temp_mail = TempMailScrapping()
        domains = temp_mail.get_all_domains()
        serializer = self.serializer_class(data=domains)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='create_temporary_email', serializer_class=TempMailSerializer)
    def create_temporary_email(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user if request.user.is_authenticated else None
        )
        return Response(serializer.data)


class MessageViewSet(
    ExtendedViewSet
):
    queryset = Message.objects.all()

    @action(methods=['post'], detail=False, url_path='check_mailbox', serializer_class=TempMailMessageSerializer)
    def check_mailbox(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        messages, bulk_messages = TempMailHelper.get_messages(
            validated_data=serializer.validated_data,
            user=request.user
        )
        serializer.save(
            messages=bulk_messages,
        )
        return Response(TempMailMessageSerializer(messages).data)

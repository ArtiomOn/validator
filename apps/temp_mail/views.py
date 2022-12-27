from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.common.views import ExtendedViewSet
from apps.temp_mail.helpers import TempMailHelper
from apps.temp_mail.models import TempMail, Message
from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping
from apps.temp_mail.serializers import (
    TempMailSerializer,
    DomainSerializer,
    TempMailMessageSerializer,
    TempRandomMailSerializer
)


class TempMailViewSet(ExtendedViewSet):
    queryset = TempMail.objects.all()
    permission_by_action = {
        'default': [AllowAny],
        'user_emails': [IsAuthenticated],
    }
    serializers_by_action = {
        'default': TempMailSerializer,
        'get_all_domains': DomainSerializer,
        'create_random_temporary_email': TempRandomMailSerializer
    }

    @action(methods=['get'], detail=False, url_path='get_all_domains')
    def get_all_domains(self, request, *args, **kwargs):
        temp_mail = TempMailScrapping()
        domains = temp_mail.get_all_domains()
        serializer = self.get_serializer(data=domains)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='create_temporary_email')
    def create_temporary_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user if request.user.is_authenticated else None
        )
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='create_random_temporary_email')
    def create_random_temporary_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # TODO fix this
        serializer.is_valid(raise_exception=True)
        username = TempMailHelper.generate_user_name()
        domain = TempMailHelper.generate_domain()
        serializer.save(
            user=request.user if request.user.is_authenticated else None,
            email_username=username,
            email_domain=domain,
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='user_emails')
    def user_emails(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(ExtendedViewSet):
    queryset = Message.objects.all()
    serializer_class = TempMailMessageSerializer
    permission_by_action = {
        'default': (AllowAny,),
    }

    @action(methods=['post'], detail=False, url_path='check_mailbox')
    def check_mailbox(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_data = TempMailHelper.get_messages(
            validated_data=serializer.validated_data,
            user=request.user
        )
        if not message_data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        messages, bulk_data = message_data
        serializer.save(
            messages=bulk_data,
        )
        return Response(TempMailMessageSerializer(messages).data)

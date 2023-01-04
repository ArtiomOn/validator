from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.common.views import ExtendedViewSet
from apps.temp_mail.helpers import TempMailHelper
from apps.temp_mail.models import TempMail
from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping
from apps.temp_mail.serializers import (
    CreateTempMailSerializer,
    TempMailMessageSerializer,
    TempMailSerializer,
    TempMailDomainSerializer
)


class TempMailViewSet(ExtendedViewSet):
    queryset = TempMail.objects.all()
    permission_by_action = {
        'default': [AllowAny],
        'user_emails': [IsAuthenticated],
    }
    serializers_by_action = {
        'default': CreateTempMailSerializer,
        'get_all_domains': TempMailDomainSerializer,
        'create_random_temporary_email': CreateTempMailSerializer,
        'user_emails': TempMailSerializer,
        'save_messages': TempMailMessageSerializer,
        'check_mailbox': TempMailMessageSerializer,
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
        username = TempMailHelper.generate_user_name()
        domain = TempMailHelper.random_domain()
        data = {
            'email_username': username,
            'email_domain': domain,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user if request.user.is_authenticated else None
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='user_emails')
    def user_emails(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='save_messages')
    def save_messages(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail_helper = TempMailHelper()
        mail_helper.get_messages(
            validated_data=serializer.validated_data,
            user=request.user
        )
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='check_mailbox')
    def check_mailbox(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = TempMail.objects.filter(
            temp_email=serializer.validated_data['temp_email']
        ).values()
        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(TempMailSerializer(queryset).data)

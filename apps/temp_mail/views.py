from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.common.views import ExtendedViewSet
from apps.temp_mail.helpers import TempMailHelper
from apps.temp_mail.models import TempMail, Domain
from apps.temp_mail.serializers import (
    CreateTempMailSerializer,
    TempMailMessageSerializer,
    TempMailSerializer,
    DomainSerializer
)

__all__ = [
    'TempMailViewSet',
]


class TempMailViewSet(ExtendedViewSet):
    queryset = TempMail.objects.all()
    permission_by_action = {
        'default': [AllowAny],
        'user_emails': [IsAuthenticated],
    }
    serializers_by_action = {
        'default': CreateTempMailSerializer,
        'get_all_domains': DomainSerializer,
        'create_random_temporary_email': CreateTempMailSerializer,
        'user_emails': TempMailSerializer,
        'save_messages': TempMailMessageSerializer,
        'check_mailbox': TempMailMessageSerializer,
    }

    def get_queryset(self):
        if self.action == 'get_all_domains':
            return Domain.objects.all()
        return super(TempMailViewSet, self).get_queryset()

    @action(methods=['get'], detail=False, url_path='get_all_domains')
    def get_all_domains(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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
        domain = Domain.objects.order_by('?').first()
        data = {
            'email_username': username,
            'email_domain_id': domain.id,
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
        ).last()
        if not queryset:
            raise ValueError('Email not found')
        return Response(TempMailSerializer(queryset).data)

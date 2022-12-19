from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from apps.common.views import ExtendedRetrieveUpdateDestroyAPIView
from apps.methods.models import Email, IMEI
from apps.methods.serializers import EmailSerializer, IMEISerializer


# noinspection DuplicatedCode
class EmailViewSet(ExtendedRetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)
    permission_by_action = {
        'user_email': [IsAuthenticated],
        'email_check': [IsAuthenticated],
        'delete': [IsAdminUser],
        'update': [IsAdminUser],
    }

    @action(detail=False, methods=['post'], url_path='email-check', url_name='email-check')
    def email_check(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # If the email is valid, then the is_valid field will be set to True
        serializer.save(
            is_valid=True,
            user=request.user,
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @email_check.mapping.get
    def user_email(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# noinspection DuplicatedCode
class IMEIViewSet(ExtendedRetrieveUpdateDestroyAPIView):
    queryset = IMEI.objects.all()
    serializer_class = IMEISerializer
    permission_classes = (IsAuthenticated,)
    permission_by_action = {
        'user_imei': [IsAuthenticated],
        'imei_check': [IsAuthenticated],
        'delete': [IsAdminUser],
        'update': [IsAdminUser],
    }

    @action(detail=False, methods=['post'], url_path='imei-check', url_name='imei-check')
    def imei_check(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # If the imei is valid, then the is_valid field will be set to True
        serializer.save(
            is_valid=True,
            user=request.user
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @imei_check.mapping.get
    def user_imei(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

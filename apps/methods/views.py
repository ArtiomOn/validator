from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.common.views import BasicModelViewSet
from apps.methods.models import Email, IMEI
from apps.methods.serializers import EmailSerializer, IMEISerializer


# noinspection DuplicatedCode
class EmailViewSet(BasicModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)
    permission_by_action = {
        'list': [IsAuthenticated],
        'create': [IsAuthenticated],
        'delete': [IsAdminUser],
        'update': [IsAdminUser],
    }

    def perform_create(self, serializer):
        # If the email is valid, then the is_valid field will be set to True
        serializer.save(
            is_valid=True
        )


# noinspection DuplicatedCode
class IMEIViewSet(BasicModelViewSet):
    queryset = IMEI.objects.all()
    serializer_class = IMEISerializer
    permission_classes = (IsAuthenticated,)
    permission_by_action = {
        'list': [IsAuthenticated],
        'create': [IsAuthenticated],
        'delete': [IsAdminUser],
        'update': [IsAdminUser],
    }

    def perform_create(self, serializer):
        # If the imei is valid, then the is_valid field will be set to True
        serializer.save(
            is_valid=True
        )

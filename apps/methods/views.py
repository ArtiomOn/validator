from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.methods.models import Email, IMEI
from apps.methods.serializers import EmailSerializer, IMEISerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)


class IMEIViewSet(viewsets.ModelViewSet):
    queryset = IMEI.objects.all()
    serializer_class = IMEISerializer
    permission_classes = (IsAuthenticated,)

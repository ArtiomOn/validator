from rest_framework.serializers import ModelSerializer
from apps.methods.models import Email, IMEI


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'


class IMEISerializer(ModelSerializer):
    class Meta:
        model = IMEI
        fields = '__all__'

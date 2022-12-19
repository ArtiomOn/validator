from rest_framework.serializers import ModelSerializer, CharField

from apps.methods.models import Email, IMEI
from apps.methods.validators.validators import EmailValidator, IMEIValidator


class EmailSerializer(ModelSerializer):
    email = CharField(
        validators=[
            EmailValidator()
        ],
        required=True,
    )

    class Meta:
        model = Email
        fields = '__all__'
        extra_kwargs = {
            'is_valid': {'read_only': True},
        }


class IMEISerializer(ModelSerializer):
    imei = CharField(
        validators=[
            IMEIValidator()
        ],
        required=True,
    )

    class Meta:
        model = IMEI
        fields = '__all__'
        extra_kwargs = {
            'is_valid': {'read_only': True},
        }

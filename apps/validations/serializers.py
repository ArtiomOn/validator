from rest_framework.serializers import ModelSerializer, CharField

from apps.validations.models import Email, IMEI
from apps.validations.validators.imei_validator import IMEIValidator
from apps.validations.validators.email_validator import EmailValidator


class EmailSerializer(ModelSerializer):
    email = CharField(
        validators=[EmailValidator()],
        required=True,
    )

    class Meta:
        model = Email
        fields = "__all__"
        extra_kwargs = {
            "is_valid": {"read_only": True},
            "user": {"read_only": True},
        }


class IMEISerializer(ModelSerializer):
    imei = CharField(
        validators=[IMEIValidator()],
        required=True,
    )

    class Meta:
        model = IMEI
        fields = "__all__"
        extra_kwargs = {
            "is_valid": {"read_only": True},
            "user": {"read_only": True},
        }

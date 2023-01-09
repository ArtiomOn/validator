from rest_framework.serializers import ModelSerializer, CharField

from apps.validations.models import Email, IMEI, JwtToken
from apps.validations.validators.imei_validator import IMEIValidator
from apps.validations.validators.email_validator import EmailValidator


__all__ = ["EmailSerializer", "IMEISerializer", "JwtTokenEncodeSerializer"]


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


class JwtTokenEncodeSerializer(ModelSerializer):
    class Meta:
        model = JwtToken
        fields = "__all__"
        extra_kwargs = {"jwt_token": {"read_only": True}, "user": {"read_only": True}}


class JwtTokenDecodeSerializer(ModelSerializer):
    class Meta:
        model = JwtToken
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "header": {"read_only": True},
        }

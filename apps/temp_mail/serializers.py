from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.temp_mail.models import TempMail, Message, Domain

__all__ = [
    "MessageSerializer",
    "TempMailSerializer",
    "TempMailMessageSerializer",
    "CreateTempMailSerializer",
    "TempMailDomainSerializer",
    "DomainSerializer",
]


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class TempMailSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = TempMail
        fields = "__all__"


class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class TempMailMessageSerializer(ModelSerializer):
    temp_email = serializers.EmailField(required=True)

    class Meta:
        model = Message
        fields = ("temp_email",)


class CreateTempMailSerializer(ModelSerializer):
    email_domain = DomainSerializer(read_only=True)
    email_domain_id = serializers.PrimaryKeyRelatedField(
        queryset=Domain.objects.all(), source="email_domain", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = TempMail
        fields = "__all__"
        extra_kwargs = {
            "temp_email": {"read_only": True},
            "user": {"read_only": True},
            "messages": {"read_only": True},
            "email_username": {"required": True},
        }


class TempMailDomainSerializer(ModelSerializer):
    email_domain = serializers.ListField(max_length=255)

    class Meta:
        model = TempMail
        fields = ("email_domain",)

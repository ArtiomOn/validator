from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.temp_mail.models import TempMail, Message
from apps.temp_mail.helpers import DomainChoices


class MessageSerializer(ModelSerializer):
    temp_email = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {
            'message_id': {'read_only': True},
            'from_email': {'read_only': True},
            'subject': {'read_only': True},
            'body': {'read_only': True},
            'retrieving_date': {'read_only': True},
            'user': {'read_only': True},
        }


class TempMailSerializer(ModelSerializer):
    email_username = serializers.CharField(required=True)
    email_domain = serializers.ChoiceField(choices=DomainChoices.DOMAIN_CHOICES, required=True)

    class Meta:
        model = TempMail
        fields = '__all__'
        extra_kwargs = {
            'temp_email': {'read_only': True},
            'user': {'read_only': True}
        }


class DomainSerializer(ModelSerializer):
    class Meta:
        model = TempMail
        fields = ('email_domain',)

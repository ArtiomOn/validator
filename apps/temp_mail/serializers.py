from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.temp_mail.models import TempMail, Message
from apps.temp_mail.helpers import DomainChoices


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class TempMailSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = TempMail
        fields = '__all__'


class TempMailMessageSerializer(ModelSerializer):
    temp_email = serializers.EmailField(required=True)

    class Meta:
        model = Message
        fields = ('temp_email',)


class CreateTempMailSerializer(ModelSerializer):
    email_username = serializers.CharField(required=True)
    # email_domain = serializers.ChoiceField(choices=DomainChoices.DOMAIN_CHOICES, required=True)
    email_domain = serializers.CharField(required=True)

    class Meta:
        model = TempMail
        fields = '__all__'
        extra_kwargs = {
            'temp_email': {'read_only': True},
            'user': {'read_only': True},
            'messages': {'read_only': True},
        }


class TempMailDomainSerializer(ModelSerializer):
    email_domain = serializers.ListField(max_length=255)

    class Meta:
        model = TempMail
        fields = ('email_domain',)

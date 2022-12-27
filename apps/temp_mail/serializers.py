from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.temp_mail.helpers import DomainChoices
from apps.temp_mail.models import TempMail, Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class TempMailMessageSerializer(Serializer):
    temp_email = serializers.EmailField(required=True)
    messages = MessageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Message.objects.bulk_update_or_create(
            validated_data['messages'],
            update_fields=['subject', 'body', 'user'],
            match_field='message_id'
        )


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


class DomainSerializer(Serializer):
    email_domain = serializers.ListField(max_length=255)

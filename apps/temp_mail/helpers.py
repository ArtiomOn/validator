import random
import string
from datetime import datetime

from django.utils.timezone import make_aware

from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping


class TempMailHelper:
    @staticmethod
    def _payload(messages, **kwargs):
        from apps.temp_mail.models import Message

        data = []
        email = kwargs.get('email')
        user = kwargs.get('user')
        for message in messages[email]:
            naive_datetime = message.get('date')
            aware_datetime = make_aware(
                datetime.strptime(naive_datetime, '%Y-%m-%d %H:%M:%S')
            )
            data.append(
                Message(
                    message_id=message.get('id'),
                    from_email=message.get('from'),
                    subject=message.get('subject'),
                    body=message.get('body'),
                    retrieving_date=aware_datetime,
                    user=user
                )
            )
        return data

    def get_messages(self, validated_data, user):
        from apps.temp_mail.models import TempMail

        mail_scrapping = TempMailScrapping()
        temp_mail = validated_data.get('temp_email')
        if not temp_mail:
            raise Exception('Email is required')
        email_username = temp_mail.split('@')[0]
        email_domain = temp_mail.split('@')[1]
        messages = mail_scrapping.check_mailbox(
            username=email_username,
            domain=email_domain
        )
        if not messages:
            return
        payload = TempMailHelper._payload(
            messages=messages,
            email=validated_data['temp_email'],
            user=user if user.is_authenticated else None
        )
        objs = self.create_message(payload)
        data = TempMail.objects.get(temp_email=temp_mail)
        if not data:
            raise Exception('Email not found')
        data.messages.add(*objs)

    @staticmethod
    def generate_user_name():
        name = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(name) for _ in range(10))
        return username

    @staticmethod
    def create_message(payload):
        from apps.temp_mail.models import Message
        return Message.objects.bulk_create(
            objs=payload,
            ignore_conflicts=True
        )

from apps.temp_mail.scrapping.scrapping import TempMail as TempMailScrapping


class DomainChoices:
    DOMAIN_CHOICES = (
        ("1secmail.com", "1secmail.com"),
        ("1secmail.org", "1secmail.org"),
        ("1secmail.net", "1secmail.net"),
        ("wwjmp.com", "wwjmp.com"),
        ("esiix.com", "esiix.com"),
        ("xojxe.com", "xojxe.com"),
        ("yoggm.com", "yoggm.com"),
    )


class TempMailHelper:
    @staticmethod
    def _payload(**kwargs):
        from apps.temp_mail.models import TempMail
        from apps.temp_mail.models import Message
        data = []
        bulk_data = []
        email = kwargs.get('email')
        user = kwargs.get('user')
        temp_email = TempMail.objects.filter(temp_email=email)
        if not temp_email.exists():
            raise Exception('Email not found')
        for message in kwargs[email]:
            data.append({
                'temp_email': email,
                'message_id': message.get('id'),
                'from_email': message.get('from'),
                'subject': message.get('subject'),
                'body': message.get('body'),
                'retrieving_date': message.get('date'),
                'user': user

            })
            bulk_data.append(Message(
                message_id=message.get('id'),
                from_email=message.get('from'),
                subject=message.get('subject'),
                body=message.get('body'),
                retrieving_date=message.get('date'),
                user=user
            ))
        data = {'messages': data, 'temp_email': email}
        return data, bulk_data

    @staticmethod
    def get_messages(validated_data, user):
        temp_mail = TempMailScrapping()
        email_username = validated_data.get('temp_email').split('@')[0]
        email_domain = validated_data.get('temp_email').split('@')[1]
        messages = temp_mail.check_mailbox(
            username=email_username,
            domain=email_domain
        )
        if not messages:
            return
        messages, bulk_messages = TempMailHelper._payload(
            **messages,
            email=validated_data['temp_email'],
            user=user if user.is_authenticated else None
        )
        return messages, bulk_messages

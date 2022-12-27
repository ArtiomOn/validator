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
    def payload(**kwargs):
        from apps.temp_mail.models import Message
        from apps.temp_mail.models import TempMail
        data = []
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
        return data

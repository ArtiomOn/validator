from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseModel

User = get_user_model()


class TempMail(BaseModel):
    temp_email = models.EmailField(blank=True, null=True, unique=True)
    email_username = models.CharField(max_length=255)
    email_domain = models.CharField(
        max_length=255,
        default='1secmail.com'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='temp_email',
        null=True,
        blank=True
    )
    messages = models.ManyToManyField(
        'Message',
        related_name='temp_email',
        blank=True,
    )

    class Meta:
        verbose_name = 'Temporary mail'
        verbose_name_plural = 'Temporary mails'
        ordering = ('-created_at',)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.temp_email = f'{self.email_username}@{self.email_domain}'
        super(TempMail, self).save(
            force_insert, force_update, using, update_fields
        )


class Message(BaseModel):
    message_id = models.IntegerField(primary_key=True)
    from_email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    retrieving_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-created_at',)

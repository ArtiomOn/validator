from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseModel
from apps.temp_mail.helpers import DomainChoices

User = get_user_model()


class TempMail(BaseModel):
    temp_email = models.EmailField(blank=True, null=True, unique=True)
    email_username = models.CharField(max_length=255)
    email_domain = models.CharField(
        max_length=255,
        choices=DomainChoices.DOMAIN_CHOICES,
        default='1secmail.com'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='temp_email',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'TempMail'
        verbose_name_plural = 'TempMails'
        ordering = ('-created_at',)

    def __str__(self):
        return self.temp_email

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
    temp_email = models.ForeignKey(TempMail, on_delete=models.CASCADE, related_name='messages', null=True)
    message_id = models.CharField(max_length=255)
    from_email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    retrieving_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-retrieving_date',)

    def __str__(self):
        return self.message_id

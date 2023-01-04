from django.db import models

from django.contrib.auth import get_user_model
from apps.common.models import BaseModel

User = get_user_model()


class Email(BaseModel):
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    is_valid = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ['created_at']

    def __str__(self):
        return self.email


class IMEI(BaseModel):
    imei = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imeis', null=True)
    is_valid = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'IMEI'
        verbose_name_plural = 'IMEIs'
        ordering = ['created_at']

    def __str__(self):
        return self.imei

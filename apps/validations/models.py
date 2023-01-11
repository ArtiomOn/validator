from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseModel

User = get_user_model()

__all__ = ["Email", "IMEI", "JwtToken"]


class Email(BaseModel):
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails")
    is_valid = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ["created_at"]

    def __str__(self):
        return self.email


class IMEI(BaseModel):
    imei = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="imeis", null=True)
    is_valid = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = "IMEI"
        verbose_name_plural = "IMEIs"
        ordering = ["created_at"]

    def __str__(self):
        return self.imei


class JwtToken(BaseModel):
    jwt_token = models.CharField(max_length=2048)
    header = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "JWT Token"
        verbose_name_plural = "JWT Tokens"
        ordering = ["created_at"]

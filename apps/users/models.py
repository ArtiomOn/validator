from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, email=None, password=None, **extra_fields):
        return super().create_superuser(
            username=email,
            email=email,
            password=password,
            **extra_fields
        )

    def create_user(self, email=None, password=None, **extra_fields):
        return super().create_user(
            username=email,
            email=email,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

User = get_user_model()

__all__ = (
    "UserRegisterSerializer",
    "UserListSerializer",
)


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "is_staff", "is_active")

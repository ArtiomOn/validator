from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

User = get_user_model()

__all__ = ["TempMailQuerySet"]


class TempMailQuerySet(QuerySet):
    def email_limit(self, user: User):
        queryset = self.filter(user=user)
        if queryset.count() >= 3:
            raise ValidationError("You have reached the limit of 3 emails")
        return queryset

    def check_users_email(self, user: User, data: dict):
        temp_email = data.get("temp_email", "")
        queryset = self.filter(user=user, temp_email=temp_email)
        if not queryset.exists():
            raise ValidationError("This email is not yours")
        return queryset.last()

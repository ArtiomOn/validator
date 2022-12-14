import json

from django.contrib.auth import get_user_model
from django.core.management import call_command
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.temp_mail.helpers import TempMailHelper
from apps.temp_mail.models import Domain

User = get_user_model()
fake = Faker()


def auth(user):
    refresh = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


class MethodsTestCase(APITestCase):
    def setUp(self) -> None:
        #  call command to create domains
        call_command("update_domains")
        self.user = User.objects.create(
            email=fake.email(),
            password="test1234",
        )

        self.domain = Domain.objects.first()

    def test_temp_mail(self):
        response = self.client.get("/temp_mail/temp_mail/get_all_domains", **auth(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            "email_username": TempMailHelper.generate_user_name(),
            "email_domain_id": self.domain.id,
        }
        response = self.client.post(
            "/temp_mail/temp_mail/create_temporary_email",
            data=data,
            **auth(user=self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            "/temp_mail/temp_mail/create_random_temporary_email",
            **auth(user=self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/temp_mail/temp_mail/user_emails", **auth(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_mailbox(self):
        email_username = TempMailHelper.generate_user_name()
        email_domain = self.domain
        temp_mail = f"{email_username}@{email_domain}"

        data = {
            "email_username": email_username,
            "email_domain_id": email_domain.id,
        }
        response = self.client.post(
            "/temp_mail/temp_mail/create_temporary_email",
            data=data,
            **auth(user=self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.temp_mail_id = json.loads(response.content).get("id")
        response = self.client.post(
            "/temp_mail/temp_mail/save_messages", data={"temp_email": temp_mail}, **auth(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            "/temp_mail/temp_mail/check_mailbox", data={"temp_email": temp_mail}, **auth(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f"/temp_mail/temp_mail/{self.temp_mail_id}", **auth(self.user))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

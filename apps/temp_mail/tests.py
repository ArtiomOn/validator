from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.temp_mail.helpers import TempMailHelper

User = get_user_model()
fake = Faker()


def auth(user=None, token=None):
    if token:
        return {
            "HTTP_AUTHORIZATION": f"Bearer {token}"
        }
    refresh = RefreshToken.for_user(user)
    return {
        "HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"
    }


class MethodsTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email=fake.email(),
            password="test1234",
        )

    def test_temp_mail(self):
        response = self.client.get(
            "/temp_mail/temp_mail/get_all_domains",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            "/temp_mail/temp_mail/create_temporary_email",
            data={
                "email_username": TempMailHelper.generate_user_name(),
                "email_domain": TempMailHelper.generate_domain(),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            "/temp_mail/temp_mail/create_random_temporary_email",
            data={},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            "/temp_mail/temp_mail/user_emails",
            **auth(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_mailbox(self):
        temp_mail = TempMailHelper.generate_user_name() + "@" + TempMailHelper.generate_domain()
        # No messages in mailbox
        response = self.client.post(
            "/temp_mail/message/check_mailbox",
            data={'temp_email': temp_mail},
            **auth(self.user)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

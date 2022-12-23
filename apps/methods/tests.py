from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from faker import Faker

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

    def test_email_check(self):
        data = {
            "email": 'test@test.com',
        }
        response = self.client.post("/methods/email/email-check", data=data, **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {
            "email": 'artiom@gmail.com',
        }
        response = self.client.post("/methods/email/email-check", data=data, **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/methods/email/email-check', **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_imei_check(self):
        data = {
            "imei": '123456789012345',
        }
        response = self.client.post("/methods/imei/imei-check", data=data, **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {
            "imei": '511557981902548',
        }
        response = self.client.post("/methods/imei/imei-check", data=data, **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/methods/imei/imei-check', **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/methods/imei/generate-imei', **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
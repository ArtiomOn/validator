from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from faker import Faker

User = get_user_model()
fake = Faker()


def auth(user=None, token=None):
    if token:
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    refresh = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email=fake.email(),
            password="test1234",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )

    def test_user_register(self):
        data = {
            "email": fake.email(),
            "password": "test1234",
        }
        response = self.client.post("/users/register", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse("user-list"), **auth(user=self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

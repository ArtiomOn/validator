from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

User = get_user_model()


def auth(user=None, token=None):
    if token:
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
    refresh = RefreshToken.for_user(user)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'
    }


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_user_register(self):
        data = {
            'email': "test@test.com",
            "password": "test1234",
        }
        response = self.client.post('/users/register', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = {
            'email': "test@test.com",
            "password": "test1234",
        }
        response = self.client.post('/users/register', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('access', None)
        response = self.client.get(reverse('user-list'), **auth(token=token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

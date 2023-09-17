from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:create")
        self.login_url = reverse("user:token_obtain_pair")
        self.me_url = reverse("user:manage")

        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_create_user(self):
        new_user_data = {
            "email": "newtestuser@example.com",
            "password": "test1password",
        }

        response = self.client.post(self.register_url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_create_user_invalid_data(self):
        invalid_data = {
            "email": "",
            "password": "testpassword",
        }
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_user_login_invalid_credentials(self):
        invalid_credentials = {
            "email": "testuser@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, invalid_credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

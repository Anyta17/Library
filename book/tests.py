from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book
from user.models import CustomUser


class BookPermissionTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email="admin@add.min",
            password="adminpassword",
            is_staff=True,
        )

        self.normal_user = CustomUser.objects.create_user(
            email="user@123.us",
            password="userpassword",
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=1.0,
        )

    def test_admin_can_create_book(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 0.5,
        }
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_cannot_create_book(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 0.5,
        }
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_users_can_list_books(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

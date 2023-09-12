from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Borrowing
from book.models import Book
from .serializers import BorrowingDetailSerializer


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            daily_fee=23,
        )

        self.borrowing = Borrowing.objects.create(
            borrow_date="2023-09-07",
            expected_return_date="2023-09-14",
            book_id=self.book,
            user_id=self.user,
        )

        self.list_url = reverse("borrowing:borrowing-list")

        self.detail_url = reverse("borrowing:borrowing-detail", args=[self.borrowing.id])

    def test_list_borrowings(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

    def test_retrieve_borrowing(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.borrowing.id)
        self.assertEqual(response.data["borrow_date"], "2023-09-07")

    def test_delete_borrowing(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Borrowing.objects.count(), 0)


class BorrowingDetailSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="tes@tuse.r",
            password="testpassword"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            daily_fee=23,
        )

        self.borrowing = Borrowing.objects.create(
            borrow_date=date(2023, 9, 7),
            expected_return_date=date(2023, 9, 14),
            actual_return_date=None,
            book_id=self.book,
            user_id=self.user,
        )

        self.serializer = BorrowingDetailSerializer(instance=self.borrowing)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id"
        })

    def test_user_id_serialization(self):
        data = self.serializer.data
        self.assertEqual(data["user_id"], self.user.id)


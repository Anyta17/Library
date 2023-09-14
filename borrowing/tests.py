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


class BorrowingCreateViewTests(TestCase):
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
            inventory=2
        )
        self.create_url = reverse("borrowing:borrowing-create")

    def test_create_borrowing(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "borrow_date": "2023-09-07",
            "expected_return_date": "2023-09-14",
            "book_id": self.book.id,
            "user_id": self.user.id,
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 1)

    def test_create_borrowing_out_of_stock(self):
        self.client.force_authenticate(user=self.user)

        self.book.inventory = 0
        self.book.save()

        data = {
            "borrow_date": "2023-09-07",
            "expected_return_date": "2023-09-14",
            "book_id": self.book.id
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["book_id"][0],
            "This book is out of stock."
        )


class BorrowingListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.admin_user = get_user_model().objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            is_staff=True
        )

        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Test Author 1",
            cover="SOFT",
            daily_fee=23,
        )

        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Test Author 2",
            cover="HARD",
            daily_fee=25,
        )

        self.borrowing1 = Borrowing.objects.create(
            borrow_date="2023-09-07",
            expected_return_date="2023-09-14",
            book_id=self.book1,
            user_id=self.user,
        )

        self.borrowing2 = Borrowing.objects.create(
            borrow_date="2023-09-10",
            expected_return_date="2023-09-17",
            book_id=self.book2,
            user_id=self.admin_user,
        )

        self.list_url = reverse("borrowing:borrowing-list")

    def test_list_borrowings_as_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_filter_borrowings_by_is_active(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.list_url, {"is_active": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_borrowings_by_user_id_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        user_id_to_filter = self.user.id
        response = self.client.get(self.list_url, {"user_id": user_id_to_filter})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_borrowings_by_user_id_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            email="regularuser@example.com",
            password="regularpassword"
        )
        self.client.force_authenticate(user=regular_user)

        user_id_to_filter = 1
        response = self.client.get(self.list_url, {"user_id": user_id_to_filter})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_borrowings_unauthenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

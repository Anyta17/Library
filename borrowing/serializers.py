from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = BookSerializer()
    user_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "book_id", "user_id")

    def create(self, validated_data):
        book = validated_data["book_id"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing

    @staticmethod
    def validate_book_id(value):
        if value.inventory == 0:
            raise serializers.ValidationError("This book is out of stock.")
        return value

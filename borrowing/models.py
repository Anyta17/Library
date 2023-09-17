from django.conf import settings
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE)
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def str(self):
        return f"Borrowed {self.book_id} by {self.user_id}"

from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hardcover"),
        ("SOFT", "Softcover"),
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(null=True, blank=True)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

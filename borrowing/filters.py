import django_filters

from .models import Borrowing


class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        method="filter_is_active",
        label="Is Active",
        help_text="Filter by active borrowings (not returned yet)",
    )
    user_id = django_filters.NumberFilter(
        method="filter_user_id",
        label="User ID",
        help_text="Filter by user ID (admin only)",
    )

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    @staticmethod
    def filter_is_active(queryset, value):
        if value:
            return queryset.filter(actual_return_date__isnull=True)
        return queryset

    def filter_user_id(self, queryset, value):
        if self.request.user.is_staff:
            return queryset.filter(user_id=value)
        return queryset.filter(user_id=self.request.user.id)

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .filters import BorrowingFilter
from .models import Borrowing
from .serializers import BorrowingDetailSerializer, BorrowingCreateSerializer


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BorrowingFilter

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def filter_queryset(self, queryset):
        user = self.request.user
        if not user.is_staff:
            return queryset.filter(user=user)
        user_id = self.request.query_params.get("user_id")
        if user_id is not None:
            return queryset.filter(user_id=user_id)
        return queryset


class BorrowingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

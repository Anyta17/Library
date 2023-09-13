from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Borrowing
from .serializers import BorrowingDetailSerializer, BorrowingCreateSerializer


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


class BorrowingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

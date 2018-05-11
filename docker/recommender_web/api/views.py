from rest_framework import generics
from .serializers import BookSerializer
from bookcrossing.models import Book


class CreateBookView(generics.ListCreateAPIView):
    """Defines the create behavior of the Book Rest API."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()

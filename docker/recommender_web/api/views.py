from rest_framework import generics
from .serializers import BookSerializer, UserSerializer, RatingSerializer
from bookcrossing.models import Book, User, Rating


class CreateBookView(generics.ListCreateAPIView):
    """Defines the create behavior of the Book Rest API"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class CreateUserView(generics.ListCreateAPIView):
    """ Defines the create behavior of the User Rest API """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class CreateRatingView(generics.ListCreateAPIView):
    """ Defines the create behavior of the Rating Rest API """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()

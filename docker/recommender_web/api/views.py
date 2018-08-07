from rest_framework import generics
from .serializers import BookSerializer, UserSerializer, RatingSerializer
from bookcrossing.models import Book, User, Rating
from .filters import RatingsFilterSet


class CreateBookView(generics.ListCreateAPIView):
    """Defines the create behavior of the Book Rest API"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailBookView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"


class CreateUserView(generics.ListCreateAPIView):
    """ Defines the create behavior of the User Rest API """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailUserView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_id"


class CreateRatingView(generics.ListCreateAPIView):
    """ Defines the create behavior of the Rating Rest API """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_class = RatingsFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailRatingView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles the GET PUT and DELETE requests for Ratings """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "rating_id"

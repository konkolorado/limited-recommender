from collections import OrderedDict

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import _reverse

from .serializers import BookSerializer, UserSerializer, RatingSerializer,  SimilaritySerializer
from .filters import RatingFilterSet, UserFilterSet, BookFilterSet, SimilarityFilterSet

from bookcrossing.models import Book, User, Rating
from recommender.models import Similarity


class BookListView(generics.ListCreateAPIView):
    """Defines the create behavior of the Book Rest API"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_class = BookFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"


class UserListView(generics.ListCreateAPIView):
    """ Defines the create behavior of the User Rest API """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new user."""
        serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class RatingListView(generics.ListCreateAPIView):
    """ Defines the create behavior of the Rating Rest API """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    # Assigning this allows the api to accept query params
    filter_class = RatingFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new rating."""
        serializer.save()


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles the GET PUT and DELETE requests for Ratings """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = "pk"


class SimilarityListView(generics.ListCreateAPIView):
    """ Defines the create behavior for the Similarity API """
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer
    filter_class = SimilarityFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new similarity."""
        serializer.save()


class SimilarityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles the GET PUT and DELETE requests for Similarities """
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer
    lookup_field = "pk"


class APIRootView(APIView):
    view_name = ('REST API')

    def get(self, request, format=None):
        '''List supported API endpoints'''

        book_api = _reverse('api-item-list', request=request)
        user_api = _reverse('api-user-list', request=request)
        rating_api = _reverse('api-rating-list', request=request)
        similarity_api = _reverse('api-similarity-list', request=request)

        data = OrderedDict()
        data['description'] = ('Limited Recommender System REST API')
        data['endpoints'] = {
            "books": book_api,
            "users": user_api,
            "ratings": rating_api,
            "similarities": similarity_api,
        }
        return Response(data)

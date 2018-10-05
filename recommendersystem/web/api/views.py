from collections import OrderedDict

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import _reverse

from .serializers import BookSerializer, UserSerializer, RatingSerializer
from bookcrossing.models import Book, User, Rating
from .filters import RatingFilterSet, UserFilterSet, BookFilterSet


class CreateBookView(generics.ListCreateAPIView):
    """Defines the create behavior of the Book Rest API"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_class = BookFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailBookView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"


class CreateUserView(generics.ListCreateAPIView):
    """ Defines the create behavior of the User Rest API """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailUserView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the GET PUT and DELETE requests for Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class CreateRatingView(generics.ListCreateAPIView):
    """ Defines the create behavior of the Rating Rest API """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    # Assigning this allows the api to accept query params
    filter_class = RatingFilterSet

    def perform_create(self, serializer):
        """Save the post data when creating a new book."""
        serializer.save()


class DetailRatingView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles the GET PUT and DELETE requests for Ratings """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = "pk"


class ApiRootView(APIView):
    view_name = ('REST API')

    def get(self, request, format=None):
        ''' List supported API versions '''

        v1 = _reverse('api_v1_root_view', request=request)
        data = OrderedDict()
        data['description'] = ('Limited Recommender System REST API')
        data['current_version'] = v1
        data['available_versions'] = dict(v1=v1)
        return Response(data)


class ApiV1RootView(APIView):
    def get(self, request, format=None):
        ''' List top level resources '''
        data = OrderedDict()
        data['books'] = _reverse('book-create', request=request)
        data['users'] = _reverse('user-create', request=request)
        data['ratings'] = _reverse('rating-create', request=request)
        return Response(data)

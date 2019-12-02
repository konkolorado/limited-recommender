from django.urls import path
from .views import (BookListView, UserListView, RatingListView,
                    SimilarityListView, SimilarityDetailView,
                    BookDetailView, UserDetailView, RatingDetailView,
                    APIRootView)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('books/', BookListView.as_view(), name="api-book-list"),
    path('books/<pk>/', BookDetailView.as_view(), name="api-book-detail"),
    path('users/', UserListView.as_view(), name="api-user-list"),
    path('users/<pk>', UserDetailView.as_view(), name="api-user-detail"),
    path('ratings/', RatingListView.as_view(), name="api-rating-list"),
    path('ratings/<pk>', RatingDetailView.as_view(),
         name="api-rating-detail"),
    path('similarities/', SimilarityListView.as_view(),
         name='api-similarity-list'),
    path('similarities/<pk>', SimilarityDetailView.as_view(),
         name='api-similarity-detail'),
]

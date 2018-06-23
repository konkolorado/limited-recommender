from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CreateBookView, CreateUserView, CreateRatingView,
                    DetailBookView, DetailUserView, DetailRatingView)

urlpatterns = {
    path('books/', CreateBookView.as_view(), name="create_book"),
    path('books/<isbn>/', DetailBookView.as_view(), name="book-detail"),
    path('users/', CreateUserView.as_view(), name="create_user"),
    path('users/<user_id>', DetailUserView.as_view(), name="user-detail"),
    path('ratings/', CreateRatingView.as_view(), name="create_rating"),
    path('ratings/<rating_id>', DetailRatingView.as_view(), name="rating-detail"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

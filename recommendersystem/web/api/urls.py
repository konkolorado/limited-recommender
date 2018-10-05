from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CreateBookView, CreateUserView, CreateRatingView,
                    DetailBookView, DetailUserView, DetailRatingView)

urlpatterns = {
    path('books/', CreateBookView.as_view(), name="book-create"),
    path('books/<pk>/', DetailBookView.as_view(), name="book-detail"),
    path('users/', CreateUserView.as_view(), name="user-create"),
    path('users/<pk>', DetailUserView.as_view(), name="user-detail"),
    path('ratings/', CreateRatingView.as_view(), name="rating-create"),
    path('ratings/<pk>', DetailRatingView.as_view(),
         name="rating-detail"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

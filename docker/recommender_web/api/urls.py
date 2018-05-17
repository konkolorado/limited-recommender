from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CreateBookView, CreateUserView, CreateRatingView,
                    DetailBookView)

urlpatterns = {
    path('books/', CreateBookView.as_view(), name="create_book"),
    path('books/<isbn>/', DetailBookView.as_view(), name="detail-book"),
    path('users/', CreateUserView.as_view(), name="create_user"),
    path('ratings/', CreateRatingView.as_view(), name="create_rating"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

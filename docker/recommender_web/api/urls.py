from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateBookView, CreateUserView, CreateRatingView

urlpatterns = {
    path('books/', CreateBookView.as_view(), name="create_book"),
    path('users/', CreateUserView.as_view(), name="create_user"),
    path('ratings/', CreateRatingView.as_view(), name="create_rating"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

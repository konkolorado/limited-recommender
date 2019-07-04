from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CreateBookView, CreateUserView, CreateRatingView,
                    DetailBookView, DetailUserView, DetailRatingView,
                    ApiRootView, ApiV1RootView)

from django.conf.urls import include

v1_urls = [
    path('', ApiV1RootView.as_view(), name="api_v1_root_view",),
    path('books/', CreateBookView.as_view(), name="api-book-create"),
    path('books/<pk>/', DetailBookView.as_view(), name="api-book-detail"),
    path('users/', CreateUserView.as_view(), name="api-user-create"),
    path('users/<pk>', DetailUserView.as_view(), name="api-user-detail"),
    path('ratings/', CreateRatingView.as_view(), name="api-rating-create"),
    path('ratings/<pk>', DetailRatingView.as_view(),
         name="api-rating-detail"),
]

urlpatterns = {
    path('', ApiRootView.as_view(), name='api_root_view'),
    path('v1/', include(v1_urls)),
}

urlpatterns = format_suffix_patterns(urlpatterns)

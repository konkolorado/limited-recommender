from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateBookView

urlpatterns = {
    url(r'^books/$', CreateBookView.as_view(), name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

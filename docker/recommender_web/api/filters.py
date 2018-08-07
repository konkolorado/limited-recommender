import django_filters
from django_filters import FilterSet
from bookcrossing.models import Rating


class RatingsFilterSet(FilterSet):
    isbn = django_filters.CharFilter(field_name='isbn__isbn',
                                     label="ISBN")
    user_id = django_filters.CharFilter(field_name='user_id__user_id',
                                        label="User ID")

    class Meta:
        model = Rating
        fields = ['isbn', 'user_id']

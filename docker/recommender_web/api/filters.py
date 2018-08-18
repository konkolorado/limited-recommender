import django_filters
from django_filters import FilterSet
from bookcrossing.models import Rating, User, Book


class RatingFilterSet(FilterSet):
    """
    Custom filter makes query params look better. Instead of
    submitting a request with the url as:
    /api/ratings/?isbn__isbn=00000&user_id__user_id=0000
    this filter allows us to instead submit:
    /api/ratings/?isbn=00000&user_id=0000
    """
    isbn = django_filters.CharFilter(field_name='isbn__isbn',
                                     label="ISBN")
    user_id = django_filters.CharFilter(field_name='user_id__user_id',
                                        label="User ID")

    class Meta:
        model = Rating
        fields = ['isbn', 'user_id']


class UserFilterSet(FilterSet):
    user_id = django_filters.CharFilter(field_name='user_id',
                                        label="User ID")

    class Meta:
        model = User
        fields = ['user_id']


class BookFilterSet(FilterSet):
    isbn = django_filters.CharFilter(field_name='isbn',
                                     label="ISBN")

    class Meta:
        model = Book
        fields = ['isbn']

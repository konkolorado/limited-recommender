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
    location = django_filters.CharFilter(field_name='location',
                                         label="Location",
                                         lookup_expr='icontains')
    age = django_filters.NumberFilter(field_name='age',
                                      label="Age")

    class Meta:
        model = User
        fields = ['user_id', 'location', 'age']


class BookFilterSet(FilterSet):
    isbn = django_filters.CharFilter(field_name='isbn',
                                     label="ISBN")
    title = django_filters.CharFilter(field_name='title',
                                      label="Title",
                                      lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author',
                                       label="Author",
                                       lookup_expr='icontains')
    publication_yr = django_filters.CharFilter(field_name='publication_yr',
                                               label="Year of Publication")
    publisher = django_filters.CharFilter(field_name='publisher',
                                          label="Publisher",
                                          lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publication_yr', 'publisher']

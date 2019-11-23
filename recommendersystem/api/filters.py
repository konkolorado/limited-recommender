import django_filters
from bookcrossing.models import Rating, User, Book
from recommender.models import Similarity


class RatingFilterSet(django_filters.FilterSet):
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
    rating = django_filters.NumberFilter(field_name="rating", label="Rating")

    class Meta:
        model = Rating
        fields = ['isbn', 'user_id', 'rating']


class UserFilterSet(django_filters.FilterSet):
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


class BookFilterSet(django_filters.FilterSet):
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


class SimilarityFilterSet(django_filters.FilterSet):
    source = django_filters.CharFilter(field_name='source__isbn',
                                       label="source")
    target = django_filters.CharFilter(field_name='target__isbn',
                                       label="target")
    score = django_filters.NumberFilter(field_name='score',
                                        label="score")

    class Meta:
        model = Similarity
        fields = ['source', 'target', 'score']

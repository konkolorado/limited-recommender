from rest_framework import serializers

from bookcrossing.models import Book, User, Rating
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class BookSerializer(serializers.ModelSerializer):
    """Serializer to map the Book model instance into JSON format."""
    isbn = serializers.CharField(trim_whitespace=True,
                                 max_length=20,
                                 validators=[
                                     UniqueValidator(
                                         queryset=Book.objects.all(),
                                         message="Cannot create Book with "
                                         "duplicate ISBN"
                                     )
                                 ])
    title = serializers.CharField(trim_whitespace=True, max_length=200)
    author = serializers.CharField(trim_whitespace=True, max_length=100)
    publication_yr = serializers.CharField(trim_whitespace=True, max_length=10)
    publisher = serializers.CharField(trim_whitespace=True, max_length=50)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        lookup_field = ("title", "author")
        fields = ("title", "author", "publication_yr", "publisher",
                  "isbn", "image_url_s", "image_url_m", "image_url_l")


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the User model instance into JSON format."""
    user_id = serializers.CharField(trim_whitespace=True,
                                    max_length=20,
                                    validators=[
                                        UniqueValidator(
                                            queryset=User.objects.all(),
                                            message="Cannot create User with "
                                            "duplicate user_id"
                                        )
                                    ])
    location = serializers.CharField(trim_whitespace=True, max_length=50)
    age = serializers.CharField(trim_whitespace=True, max_length=3)

    class Meta:
        model = User
        fields = ("user_id", "age", "location")


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Rating model instance into JSON format."""

    class Meta:
        model = Rating
        fields = ("user_id", "isbn", "rating", "created", "last_modified")
        read_only_fields = ("created", "last_modified")
        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=('user_id', 'isbn'),
                message="Cannot create duplicate rating on a prexisting "
                "user_id and isbn pair"
            )
        ]
        extra_kwargs = {
            'isbn': {'view_name': 'book-detail', 'lookup_field': 'isbn'},
            'user_id': {'view_name': 'user-detail', 'lookup_field': 'user_id'},
        }

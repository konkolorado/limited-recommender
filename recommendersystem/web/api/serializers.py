from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from bookcrossing.models import Book, User, Rating
from api.custom_fields import (HyperlinkedUserIDIdentityField,
                               HyperlinkedISBNIdentityField)
from api.fields import UserIDSlugRelatedField, ISBNSlugRelatedField


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
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        lookup_field = ("title", "author")
        fields = ("id", "title", "author", "publication_yr", "publisher",
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
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = ("id", "user_id", "age", "location")


class RatingSerializer(serializers.ModelSerializer):
    """Serializer to map the Rating model instance into JSON format."""
    user_id = UserIDSlugRelatedField(slug_field='user_id',
                                     queryset=User.objects.all())
    isbn = ISBNSlugRelatedField(slug_field='isbn',
                                queryset=Book.objects.all())

    isbn_url = HyperlinkedISBNIdentityField(view_name='book-detail',
                                            lookup_field="pk")
    user_id_url = HyperlinkedUserIDIdentityField(view_name='user-detail',
                                                 lookup_field="pk")
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Rating
        lookup_field = "id"

        # Hyper linked fields read only by default
        fields = ("id", "user_id", "isbn",  "rating",
                  "user_id_url", "isbn_url", "created", "last_modified")

        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=('user_id', 'isbn'),
                message="Cannot create duplicate rating on a prexisting "
                "User ID and ISBN pair"
            )
        ]

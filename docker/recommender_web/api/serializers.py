from rest_framework import serializers

from bookcrossing.models import Book, User, Rating


class BookSerializer(serializers.ModelSerializer):
    """Serializer to map the Book model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        lookup_field = ("title", "author")
        fields = ("title", "author", "publication_yr", "publisher",
                  "isbn", "image_url_s", "image_url_m", "image_url_l")
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the User model instance into JSON format."""

    class Meta:
        model = User
        fields = ("user_id", "age", "location")
        read_only_fields = ("id",)


class RatingSerializer(serializers.ModelSerializer):
    """Serializer to map the Rating model instance into JSON format."""
    user_id = serializers.SlugRelatedField(
        slug_field='user_id',
        required=True,
        queryset=User.objects.all()
    )
    isbn = serializers.SlugRelatedField(
        slug_field='title',
        required=True,
        queryset=Book.objects.all()
    )

    class Meta:
        model = Rating
        fields = ("user_id", "isbn", "rating")

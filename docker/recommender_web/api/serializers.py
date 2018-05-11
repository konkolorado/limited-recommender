from rest_framework import serializers

from bookcrossing.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        fields = ("isbn", "title",
                  "author", "publication_yr", "publisher",
                  "image_url_s", "image_url_m", "image_url_l")
        read_only_fields = ("id",)

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from bookcrossing.models import Book, User, Rating
from recommender.models import Similarity

from api.custom_fields import (HyperlinkedUserIDIdentityField,
                               HyperlinkedISBNIdentityField)
from api.fields import UserIDSlugRelatedField, ISBNSlugRelatedField
from api.validators import validate_all_digits


class BookSerializer(serializers.ModelSerializer):
    """Serializer to map the Book model instance into JSON format."""
    isbn = serializers.CharField(trim_whitespace=True,
                                 max_length=20,
                                 validators=[
                                     UniqueValidator(
                                         queryset=Book.objects.all(),
                                         message="Cannot create Book with "
                                         "duplicate ISBN"),
                                     validate_all_digits,
                                 ])
    title = serializers.CharField(trim_whitespace=True, max_length=200)
    author = serializers.CharField(trim_whitespace=True, max_length=100)
    publication_yr = serializers.CharField(trim_whitespace=True, max_length=10,
                                           validators=[validate_all_digits])
    publisher = serializers.CharField(trim_whitespace=True, max_length=50)
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the User model instance into JSON format."""
    user_id = serializers.CharField(trim_whitespace=True,
                                    max_length=20,
                                    validators=[
                                        UniqueValidator(
                                            queryset=User.objects.all(),
                                            message="Cannot create User with "
                                            "duplicate user_id"
                                        ),
                                        validate_all_digits,
                                    ])
    location = serializers.CharField(trim_whitespace=True, max_length=50)
    age = serializers.CharField(trim_whitespace=True, max_length=3,
                                validators=[validate_all_digits])
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    """Serializer to map the Rating model instance into JSON format."""
    user_id = UserIDSlugRelatedField(slug_field='user_id',
                                     queryset=User.objects.all())
    isbn = ISBNSlugRelatedField(slug_field='isbn',
                                queryset=Book.objects.all())

    isbn_url = HyperlinkedISBNIdentityField(view_name='api-book-detail',
                                            lookup_field="pk")
    user_id_url = HyperlinkedUserIDIdentityField(view_name='api-user-detail',
                                                 lookup_field="pk")
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=('user_id', 'isbn'),
                message="Cannot create duplicate rating on a prexisting "
                "User ID and ISBN pair"
            )
        ]


class SimilaritySerializer(serializers.ModelSerializer):
    """ Serializer to map Similarity model instances to/from JSON """
    source = serializers.HyperlinkedRelatedField(view_name='api-book-detail',
                                                 read_only=True,
                                                 lookup_field="pk")
    target = serializers.HyperlinkedRelatedField(view_name='api-book-detail',
                                                 read_only=True,
                                                 lookup_field="pk")
    score = serializers.FloatField(max_value=1.0, min_value=0.0)

    class Meta:
        model = Similarity
        fields = '__all__'

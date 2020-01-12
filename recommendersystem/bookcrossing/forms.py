from django.forms import ModelForm, ModelChoiceField

from .models import Book, User, Rating


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publication_yr', 'publisher',
                  'image_url_s']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'location', 'age']


class RatingForm(ModelForm):
    # This code uses to_field_name to correctly use the foreign key's non-pk
    # field to perform the lookup/validation
    user_id = ModelChoiceField(queryset=User.objects.all(),
                               to_field_name="user_id")
    isbn = ModelChoiceField(queryset=Book.objects.all(), to_field_name="isbn")

    class Meta:
        model = Rating
        fields = ['user_id', 'isbn', 'rating']

from django.forms import ModelForm

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
    class Meta:
        model = Rating
        fields = ['user_id', 'isbn', 'rating']

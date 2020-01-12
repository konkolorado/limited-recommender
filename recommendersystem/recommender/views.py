from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.urls import reverse

from bookcrossing.models import Book, User, Rating
from bookcrossing.forms import BookForm, UserForm, RatingForm
from recommender.models import Similarity

PAGE_ITEMS = 10


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request,
                      self.template_name,
                      context={'api_url': reverse('api-root'),
                               'user_url': reverse('user-list'),
                               'item_url': reverse('item-list'),
                               'rating_url': reverse('rating-list'),
                               'similarity_url': reverse('similarity-list')})


class UserListView(FormMixin, ListView):
    model = User
    form_class = UserForm
    paginate_by = PAGE_ITEMS
    # Default: object_list
    context_object_name = 'users'
    # Default: <app_label>/<model_name>_list.html
    template_name = 'user_list.html'


class ItemListView(FormMixin, ListView):
    model = Book
    form_class = BookForm
    paginate_by = PAGE_ITEMS
    context_object_name = 'items'
    template_name = 'item_list.html'


class RatingListView(FormMixin, ListView):
    model = Rating
    form_class = RatingForm
    paginate_by = PAGE_ITEMS
    context_object_name = 'ratings'
    template_name = 'rating_list.html'


class SimilarityListView(ListView):
    model = Similarity
    paginate_by = PAGE_ITEMS
    context_object_name = 'similarities'
    template_name = 'similarity_list.html'

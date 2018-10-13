from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator


from bookcrossing.models import Book, User, Rating

import sys


def index(request):
    books = Book.objects.all()
    books_paginator = Paginator(books, 5)
    book_request_page = request.GET.get('book_page')
    book_page = books_paginator.get_page(book_request_page)

    ratings = Rating.objects.all()
    ratings_pagintor = Paginator(ratings, 5)
    rating_request_page = request.GET.get('rating_page')
    rating_page = ratings_pagintor.get_page(rating_request_page)

    users = User.objects.all()
    users_paginator = Paginator(users, 5)
    user_request_page = request.GET.get('user_page')
    user_page = users_paginator.get_page(user_request_page)

    # Determine which page was actually requested to set that
    # tab as active in the html. Defaults to book being active
    user_active = user_request_page is not None
    rating_active = rating_request_page is not None
    book_active = book_request_page is not None or \
        (not user_active and not rating_active)

    return render(request, 'index.html', {'users': user_page,
                                          'books': book_page,
                                          'ratings': rating_page,
                                          'user_active': user_active,
                                          'rating_active': rating_active,
                                          'book_active': book_active})

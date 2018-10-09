from django.shortcuts import render_to_response

from bookcrossing.models import Book, User, Rating


def index(request):

    users = User.objects.all()
    for u in users:
        u.location = u.location.split(',')[-1].upper()
        if u.age == "unk":
            u.age = "unknown"

    context = {
        "books": Book.objects.all(),
        "users": users,
        "ratings": Rating.objects.all()
    }
    return render_to_response("index.html", context)

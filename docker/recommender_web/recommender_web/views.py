from django.shortcuts import render_to_response

import datetime

def index(request):
    context = {
        "now": datetime.datetime.now(),
    }
    return render_to_response("index.html", context)

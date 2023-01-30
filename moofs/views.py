import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render, redirect

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request)
    #username = None
    #if request.user.is_authenticated:
    #    username = request.user.username
    #return render(request, "pages/feed.html", context={"username": username}, status=200)
    return render(request, "pages/feed.html")

def moofs_list_view(request, *args, **kwargs):
    return render(request, "moofs/list.html")

def moofs_detail_view(request, moof_id, *args, **kwargs):
    return render(request, "moofs/detail.html", context={"moof_id": moof_id})



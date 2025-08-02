from django.http import HttpRequest
from django.shortcuts import render

template_name = "home.html"


def home(request: HttpRequest, *args, **kwargs):
    return render(request, template_name)

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/home.html")


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about_us.html")


def contact_us(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/contact_us.html")


def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/privacy_policy.html")

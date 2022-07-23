from django.shortcuts import render


def index(request):
    return render(request, "pages/index.html")


def about_us(request):
    return render(request, "pages/about_us.html")


def contact_us(request):
    return render(request, "pages/contact_us.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")

from django.shortcuts import render


def index(request):
    print(request.session)
    greeting = "I don't know who you are!"
    if request.user.is_authenticated:
        greeting = f'Hello {request.user.get_full_name()}'
    return render(request, "pages/index.html", context={
        "greeting": greeting
    })


def about_us(request):
    return render(request, "pages/about_us.html")


def contact_us(request):
    return render(request, "pages/contact_us.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")

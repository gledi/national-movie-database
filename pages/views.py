from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import stripe


def index(request):
    greeting = "I don't know who you are!"
    if request.user.is_authenticated:
        greeting = f"Hello {request.user.get_full_name()}"
    return render(request, "pages/index.html", context={"greeting": greeting})


def about_us(request):
    return render(request, "pages/about_us.html")


def contact_us(request):
    return render(request, "pages/contact_us.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def shop(request):
    return render(request, "pages/shop.html", context={})


@csrf_exempt
def get_stripe_pubkey(request):
    if request.method == "GET":
        pub_key = settings.STRIPE_PUBLISHABLE_KEY
        return JsonResponse({"publicKey": pub_key})


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                + "payments/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "payments/cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "unit_amount": 2000,
                            "product_data": {
                                "name": "T-Shirt",
                                "description": "Comfortable cotton t-shirt",
                            },
                        },
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


from movies.models import Movie, Purchase


def payment_success(request):
    movie_id = request.GET.get("movie_id")
    if movie_id is not None:
        pk = int(movie_id)
        quantity = int(request.GET.get("quantity"))
        movie = Movie.objects.get(pk=pk)
        Purchase.objects.create(
            movie=movie,
            quantity=quantity,
            purchased_on=timezone.now(),
        )
    return render(request, "pages/payment_success.html")


def payment_cancel(request):
    return render(request, "pages/payment_cancelled.html")


import sqlite3


class Migration:
    def __init__(self, id, app, name, applied):
        self.id = self.pk = id
        self.app = app
        self.name = name
        self.applied = applied

    def __str__(self):
        return f"{self.pk}. {self.app}.{self.name}"


def get_django_migrations(request):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    sql_query = "SELECT id, app, name, applied FROM django_migrations"

    cur.execute(sql_query)
    migrations = [Migration(*row) for row in cur]

    html_parts = [
        "<table>"
        "<thead><tr>"
        "<th>ID</th>"
        "<th>App</th>"
        "<th>Name</th>"
        "<th>Applied</th>"
        "</tr></thead>"
        "<tbody>"
    ]

    for migration in migrations:
        html_parts.append(
            "<tr>"
            f"<td>{migration.id}.</td>"
            f"<td>{migration.app}</td>"
            f"<td>{migration.name}</td>"
            f"<td>{migration.applied}</td>"
            "</tr>"
        )

    html_parts.append("</tbody></table>")

    cur.close()
    conn.close()

    return HttpResponse("".join(html_parts))

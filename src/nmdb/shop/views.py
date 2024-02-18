from http import HTTPStatus

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST
from rest_framework.reverse import reverse

from .cart import Cart
from .forms import CartUpdateForm
from .models import Product


@login_required
def get_product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "shop/product_list.html", context={"products": products})


@login_required
def cart_detail(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/cart_detail.html")


@login_required
def payment_succeeded(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "shop/payment_succeeded.html")


@login_required
def payment_cancelled(request):
    return render(request, "shop/payment_cancelled.html")


@login_required
@require_POST
def cart_update(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    form = CartUpdateForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"detail": _("Invalid quantity")},
            status=HTTPStatus.BAD_REQUEST,
        )

    cart = Cart(request)
    cart.update(product=product, quantity=form.cleaned_data["quantity"])
    return JsonResponse({"detail": _("Shopping cart updated")})


@login_required
@require_POST
def cart_empty(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    cart.clear()
    return JsonResponse({"detail": _("Shopping cart cleared")})


@login_required
@require_GET
def get_stripe_pubkey(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"publicKey": settings.STRIPE_PUBLISHABLE_KEY})


@login_required
@require_GET
def create_checkout_session(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []
    for item in cart.items():
        line_items.append(
            {
                "price_data": {
                    "currency": item["currency"],
                    "unit_amount": int(item["price"] * 100),
                    "product_data": {
                        "name": item["name"],
                        "description": item["description"],
                        "images": [
                            "http://localhost:8000" + item["image"][1:],
                        ],
                    },
                },
                "quantity": int(item["quantity"]),
            }
        )

    try:
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect
        # will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=reverse("shop:payment-success", request=request)
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=reverse("shop:payment-cancel", request=request),
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
        )
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

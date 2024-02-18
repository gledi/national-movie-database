from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("products/", views.get_product_list, name="product-list"),
    path("cart/", views.cart_detail, name="cart-detail"),
    path("cart/update/", views.cart_update, name="cart-update"),
    path("cart/empty/", views.cart_empty, name="cart-empty"),
    path("payments/pubkey/", views.get_stripe_pubkey, name="payments-pubkey"),
    path(
        "payments/checkout-session/",
        views.create_checkout_session,
        name="payments-checkout-session",
    ),
    path("payments/succeeded/", views.payment_succeeded, name="payment-success"),
    path("payments/cancelled/", views.payment_cancelled, name="payment-cancel"),
]

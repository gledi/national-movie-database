from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about_us, name="about"),
    path("contact-us/", views.contact_us, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy"),
    path("django-migrations/", views.get_django_migrations),
    path("shop/", views.shop, name="shop"),
    path("payments/pubkey/", views.get_stripe_pubkey, name="payments_pubkey"),
    path(
        "payments/checkout-session/",
        views.create_checkout_session,
        name="payments_checkout_session",
    ),
    path("payments/success/", views.payment_success, name="payment_success"),
    path("payments/cancelled/", views.payment_cancel, name="payment_cancel"),
]

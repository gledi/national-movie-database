import logging
from decimal import Decimal
from typing import TypedDict

from django.conf import settings
from django.http import HttpRequest

from .models import Product

logger = logging.getLogger(__name__)


class CartItem(TypedDict):
    key: str
    user_id: int
    product_id: int
    name: str
    description: str | None
    quantity: int
    price: Decimal
    currency: str
    image: str | None


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.session = request.session
        cart: dict[str, CartItem] | None = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def items(self) -> list[CartItem]:
        return list(self.cart.values())

    def update(self, product: Product, quantity: int = 1) -> None:
        if quantity == 0:
            logger.error("Tried to update cart with quantity 0")
            return

        action = self.add if quantity > 0 else self.remove
        quantity *= 1 if quantity > 0 else -1

        action(product=product, quantity=quantity)

    def add(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the cart or increment its quantity."""
        key = str(product.pk)

        if key in self.cart:
            self.cart[key]["quantity"] = self.cart[key].get("quantity", 0) + quantity
        else:
            self.cart[key] = {
                "key": key,
                "user_id": self.request.user.id,
                "product_id": product.pk,
                "name": product.name,
                "description": product.description,
                "quantity": 1,
                "price": product.price,
                "image": product.image.url,
            }

        self.save()

    def remove(self, product: Product, quantity: int = 1) -> None:
        """Remove product from cart or decrement its quantity."""
        key = str(product.pk)
        if key in self.cart:
            self.cart[key]["quantity"] = self.cart[key].get("quantity", 0) - quantity
            if self.cart[key]["quantity"] < 1:
                del self.cart[key]

            self.save()
        else:
            logger.error(
                "%r tried to remove %r that was not on the cart",
                self.request.user,
                product,
            )

    def save(self) -> None:
        """Update cart and mark session as modified."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self) -> None:
        """Empties the cart."""
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def total_amount(self) -> float:
        total = 0.0
        for key, value in self.cart.items():
            total += float(value["price"]) * value["quantity"]
        return total

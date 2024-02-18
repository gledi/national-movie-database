from typing import Any

from .cart import Cart


def cart_total_amount(request) -> dict[str, Any]:
    if request.user.is_authenticated:
        cart = Cart(request)
        return {"cart_total_amount": cart.total_amount}
    else:
        return {"cart_total_amount": 0}

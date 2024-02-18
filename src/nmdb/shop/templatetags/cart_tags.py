from django import template

register = template.Library()


@register.filter()
def multiply(value, arg):
    return float(value) * arg


@register.filter
def total_amount(value):
    total = 0
    for key, product in value.items():
        total += float(product["price"]) * int(product["quantity"])

    return total

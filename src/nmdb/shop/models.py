from django.db import models
from django.utils.translation import gettext_lazy as _

from nmdb.core.models import BaseModel


class Product(BaseModel):
    class Currencies(models.TextChoices):
        EUR = "eur", ""
        USD = "usd", "$"
        GBP = "gbp", ""
        ALL = "all", "L"

    name = models.CharField(_("name"), max_length=255)
    image = models.ImageField(_("image"), upload_to="products/", null=True, blank=True)
    price = models.DecimalField(_("price"), max_digits=8, decimal_places=2)
    currency = models.CharField(
        _("currency"),
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.EUR,
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "products"
        verbose_name = _("product")
        verbose_name_plural = _("products")

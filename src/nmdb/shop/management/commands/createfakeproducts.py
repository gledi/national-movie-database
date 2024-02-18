import io
import random

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from nmdb.shop.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=10)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()

        products = []
        for i in range(options["count"]):
            name = fake.sentence()
            filename = f"{slugify(name)}_{i}.png"
            product = Product(
                name=name,
                description="\n".join(fake.paragraphs()),
                price=random.randrange(5, 121) + 0.99,
                image=ImageFile(io.BytesIO(fake.image(size=(320, 400))), name=filename),
            )
            products.append(product)

        Product.objects.bulk_create(products)

import io
import random
import secrets
import time

import requests
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from nmdb.movies.models import Person
from nmdb.photos.models import Photo

IMAGE_URL = "https://thispersondoesnotexist.com/image"


class Command(BaseCommand):
    def handle(self, **options):
        fake = Faker()
        people = Person.objects.all()

        photos = []
        for person in people:
            resp = requests.get(IMAGE_URL)
            raw_img = resp.content

            filename = (
                f"{slugify(person.name).replace('-', '_')}"
                f"_{person.pk}_{secrets.token_hex(3)}.jpg".lower()
            )
            photo = Photo(
                content_object=person,
                photo=ImageFile(io.BytesIO(raw_img), name=filename),
                caption=fake.bs(),
                is_primary=True,
            )
            photos.append(photo)
            time.sleep(random.randrange(3, 7) / 10)

        Photo.objects.bulk_create(photos)

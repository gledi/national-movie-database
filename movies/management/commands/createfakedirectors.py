import io
import random

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from faker import Faker

from movies.models import Director


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=10)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()

        directors = []
        for i in range(options["count"]):
            first_name = fake.first_name()
            last_name = fake.last_name()
            filename = f'{first_name}_{last_name}_{i}.png'.lower()
            director = Director(
                first_name=first_name,
                last_name=last_name,
                bio='\n'.join(fake.paragraphs(6)),
                birthdate=fake.date_between('-80y', '-20y'),
                photo=ImageFile(io.BytesIO(fake.image()), name=filename),
            )
            directors.append(director)

        Director.objects.bulk_create(directors)

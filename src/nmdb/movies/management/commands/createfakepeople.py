import random

from django.core.management.base import BaseCommand
from faker import Faker

from nmdb.movies.models import Person


class Command(BaseCommand):
    help = "Creates fake people to use as directors, actors, etc."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=20)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()

        people: list[Person] = []
        for i in range(options["count"]):
            name = fake.name()
            person = Person(
                name=name,
                bio="\n".join(fake.paragraphs(random.randrange(3, 10))),
                birthdate=fake.date_between("-80y", "-20y"),
            )
            people.append(person)

        Person.objects.bulk_create(people)

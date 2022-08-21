import random

from django.core.management.base import BaseCommand
from faker import Faker

from movies.models import Movie, Director


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=10)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()
        directors = Director.objects.all()

        movies = []
        for i in range(options["count"]):
            movie = Movie(
                title=fake.sentence(),
                year=int(fake.year()),
                runtime=random.randrange(60, 180),
                plot='\n'.join(fake.paragraphs()),
                rating=random.choice(Movie.RATINGS)[0],
                director=random.choice(directors),
            )
            movies.append(movie)

        Movie.objects.bulk_create(movies)

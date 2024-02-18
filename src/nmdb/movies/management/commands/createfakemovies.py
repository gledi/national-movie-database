import io
import random

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from nmdb.movies.models import Movie, Person, Role


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=10)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()
        people = Person.objects.all()

        movies: list[Movie] = []
        for i in range(options["count"]):
            title = fake.sentence()[:-1]
            slug = slugify(title)
            movie = Movie(
                title=title,
                slug=slug,
                year=int(fake.year()),
                runtime=random.randrange(60, 180),
                plot="\n\n".join(fake.paragraphs(random.randrange(3, 5))),
                mpaa_rating=random.choice(Movie.Ratings.values),
                director=random.choice(people),
            )
            movies.append(movie)

        Movie.objects.bulk_create(movies)

        for movie in movies:
            movie.tags.add(*fake.bs().split())

            for i in range(random.randrange(1, 21)):
                filename = f"{movie.slug.replace('-', '_')}_{movie.pk}_{i}.png".lower()
                movie.photos.create(
                    photo=ImageFile(io.BytesIO(fake.image((768, 1024))), name=filename),
                    caption=fake.bs(),
                    is_primary=i == 0,
                )

            people = [person for person in people]
            roles = []
            for actor in random.sample(people, k=random.randrange(5, 11)):
                roles.append(Role(movie=movie, actor=actor, role=fake.name()))
            Role.objects.bulk_create(roles)

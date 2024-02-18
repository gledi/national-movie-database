import datetime as dt
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker

from nmdb.news.models import Post

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=10)
        return super().add_arguments(parser)

    def handle(self, **options):
        fake = Faker()

        reporters = Group.objects.prefetch_related("user_set").get(name="Reporters")

        users = [user for user in reporters.user_set.all()]

        posts = []
        for _ in range(options["count"]):
            title = fake.bs().title()
            published = fake.pybool()
            published_on = None
            if published:
                start_days = -3 * options["count"]
                published_on = timezone.make_aware(
                    fake.date_time_between_dates(
                        dt.timedelta(days=start_days),
                        dt.timedelta(-1),
                    )
                )

            post = Post(
                title=title,
                slug=slugify(title),
                body="\n\n".join(
                    fake.paragraph(random.randrange(4, 9), True)
                    for _ in range(random.randrange(10, 30))
                ),
                author=random.choice(users),
                is_published=published,
                published_on=published_on,
            )
            posts.append(post)

        Post.objects.bulk_create(posts)

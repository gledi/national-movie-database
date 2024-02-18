from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create some groups/users/perms to initialize the site."

    def handle(self, **options):
        contributors, created = Group.objects.update_or_create(name="Contributors")
        self._w("Group", contributors.name, created)
        moderators, created = Group.objects.update_or_create(name="Moderators")
        self._w("Group", moderators.name, created)
        reporters, created = Group.objects.update_or_create(name="Reporters")
        self._w("Group", reporters.name, created)

        dummy_users = [
            ("admin@nmdb.al", "Admin Nmdb", {"is_staff": True, "is_superuser": True}),
            ("alban@nmdb.al", "Alban Nmdb", {"is_staff": True}),
            ("ana@nmdb.al", "Ana Nmdb", {"is_staff": True}),
            ("jlennon@beatles.org", "John Lennon"),
            ("pmccartney@beatles.org", "Paul McCartney"),
            ("gharrison@beatles.org", "George Harrison"),
            ("rstarr@beatles.org", "Ringo Starr"),
            ("mjagger@rollingstones.net", "Mick Jagger"),
            ("krichards@rollingstones.net", "Keith Richards"),
            ("jhendrix@experience.com", "Jimi Hendrix"),
            ("oosbourne@sabbath.io", "Ozzy Osbourne"),
            ("tiommi@sabbath.io", "Tony Iommi"),
            ("rhalford@priest.org", "Rob Halford"),
        ]
        users = []
        for email, name, *rest in dummy_users:
            defaults = {"name": name}
            if rest:
                for elem in rest:
                    defaults.update(elem)
            user, created = User.objects.update_or_create(
                email=email, defaults=defaults
            )
            self._w("User", email, created)
            if created:
                user.set_password("pass123")
                users.append(user)

        if users:
            User.objects.bulk_update(users, fields=["password"])

    def _w(self, model_name: str, obj: str, created: bool) -> None:
        fmt = "{} {!r} was {} successfully"
        msg = fmt.format(model_name, obj, "created" if created else "updated")
        style_func = self.style.SUCCESS if created else self.style.WARNING
        self.stdout.write(msg, style_func, ending="\n")

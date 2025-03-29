from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nmdb.users"

    def ready(self) -> None:
        from . import signals  # noqa: F401

        return super().ready()

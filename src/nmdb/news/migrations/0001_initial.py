# Generated by Django 4.1.3 on 2022-11-17 10:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="updated at",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("slug", models.SlugField(max_length=255, verbose_name="slug")),
                ("body", models.TextField(verbose_name="body")),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="is published?"),
                ),
                (
                    "published_on",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="published on"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="author",
                    ),
                ),
            ],
            options={
                "verbose_name": "post",
                "verbose_name_plural": "posts",
                "db_table": "posts",
            },
        ),
    ]
# Generated by Django 4.1.3 on 2022-11-17 10:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
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
                (
                    "photo",
                    models.ImageField(
                        upload_to="photos/%Y/%m/%d", verbose_name="photo"
                    ),
                ),
                (
                    "caption",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="caption"
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False, verbose_name="is primary"),
                ),
                ("object_id", models.BigIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "photo",
                "verbose_name_plural": "photos",
                "db_table": "photos",
            },
        ),
    ]

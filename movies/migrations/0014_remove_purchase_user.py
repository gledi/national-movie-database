# Generated by Django 4.1.1 on 2022-09-17 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0013_movie_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchase",
            name="user",
        ),
    ]

# Generated by Django 4.1 on 2022-08-20 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_review_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='content',
            field=models.TextField(null=True),
        ),
    ]

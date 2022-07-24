from django.db import models
from django.urls import reverse


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    birthdate = models.DateField(null=True)
    photo = models.ImageField(null=True, upload_to="directors")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = "directors"


class Movie(models.Model):
    RATINGS = [
        ("G", "G - General Audiences"),
        ("PG", "PG - Parental Guidance Suggesteds"),
        ("PG-13", "PG-13 - Parents Strongly Cautioned"),
        ("R", "R - Restricted"),
        ("NC-17", "NC-17 – Adults Only"),
    ]

    title = models.CharField(max_length=255)
    year = models.IntegerField()
    runtime = models.IntegerField()
    plot = models.TextField(null=True)
    rating = models.CharField(max_length=10, choices=RATINGS)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    # director_id = models.IntegerField()
    actors = models.ManyToManyField('movies.Actor')

    class Meta:
        db_table = "movies"

    def __str__(self):
        return f'{self.title} ({self.year})'

    def get_absolute_url(self):
        return reverse("movie-detail", kwargs={"pk": self.pk})


class Actor(models.Model):
    name = models.CharField(max_length=100, null=False)
    bio = models.TextField(null=True)

    class Meta:
        db_table = "actors"

    def __str__(self):
        return self.name

# CREATE TABLE movies_actor (
#     id int not null,
#     name varchar(100) not null,
#     bio text null,
#     constraint pk_actors primary key (id)
# )

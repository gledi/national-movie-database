from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = "directors"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    runtime = models.IntegerField()
    plot = models.TextField(null=True)
    rating = models.CharField(max_length=10)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    # director_id = models.IntegerField()
    actors = models.ManyToManyField('movies.Actor')

    class Meta:
        db_table = "movies"

    def __str__(self):
        return f'{self.title} ({self.year})'


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

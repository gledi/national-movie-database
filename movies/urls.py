from django.urls import path

from . import views


urlpatterns = [
    path("movies/", views.get_movie_list, name="movie-list"),
    path("movies/add/", views.add_movie, name="movie-add"),
]

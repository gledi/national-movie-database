from django.urls import path

from . import views


app_name = "apiv1"

urlpatterns = [
    path("movies/", views.get_movie_list, name="movie-list"),
    path("movies/<int:pk>/", views.get_movie_details, name="movie-detail"),
]


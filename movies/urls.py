from django.urls import path

from . import views


urlpatterns = [
    path("movies/", views.get_movie_list, name="movie-list"),
    path("movies/add/", views.add_movie, name="movie-add"),
    path("movies/<int:pk>/", views.get_movie_detail, name="movie-detail"),
    path("movies/<int:pk>/edit/", views.edit_movie, name='movie-edit'),
    path("movies/<int:pk>/delete/", views.delete_movie, name='movie-delete'),
]

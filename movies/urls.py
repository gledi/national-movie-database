from django.urls import path

from . import views


urlpatterns = [
    path("movies/", views.get_movie_list, name="movie-list"),
    path("movies/add/", views.add_movie, name="movie-add"),
    path("movies/<int:pk>/", views.get_movie_detail, name="movie-detail"),
    path("movies/<int:pk>/edit/", views.edit_movie, name='movie-edit'),
    path("movies/<int:pk>/delete/", views.delete_movie, name='movie-delete'),

    path("directors/", views.get_director_list, name="director-list"),
    path("directors/add/", views.add_director, name="director-add"),
    path("directors/<int:pk>/", views.get_director_detail, name="director-detail"),
    path("directors/<int:pk>/edit/", views.edit_director, name='director-edit'),
    path("directors/<int:pk>/delete/", views.delete_director, name='director-delete'),
]

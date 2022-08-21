from django.urls import path

from . import views2


app_name = "apiv1"

urlpatterns = [
    path("movies/", views2.MovieListCreateView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", views2.MovieDetailUpdateDeleteView.as_view(), name="movie-detail"),
]

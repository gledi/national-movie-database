from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path("", views.MovieListView.as_view(), name="movie-list"),
    path("add/", views.MovieCreateView.as_view(), name="movie-add"),
    path("<slug>/", views.MovieDetailView.as_view(), name="movie-detail"),
    path("<slug>/edit/", views.MovieUpdateView.as_view(), name="movie-edit"),
    path("<slug>/delete/", views.MovieDeleteView.as_view(), name="movie-delete"),
    path("<int:pk>/review/", views.review_movie, name="movie-review"),
]

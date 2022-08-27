from django.urls import path

from . import views


urlpatterns = [
    # path("movies/", views.get_movie_list, name="movie-list"),
    path("movies/", views.MovieListView.as_view(), name="movie-list"),
    path("movies/add/", views.add_movie, name="movie-add"),
    # path("movies/add/", views.MovieCreateView.as_view(), name="movie-add"),
    path("movies/<int:pk>/", views.get_movie_detail, name="movie-detail"),
    # path("movies/<int:pk>/", views.MovieDetailView.as_view(), name="movie-detail"),
    # path("movies/<int:pk>/edit/", views.edit_movie, name='movie-edit'),
    path("movies/<int:pk>/edit/", views.MovieUpdateView.as_view(), name="movie-edit"),
    # path("movies/<int:pk>/delete/", views.delete_movie, name='movie-delete'),
    path(
        "movies/<int:pk>/delete/", views.MovieDeleteView.as_view(), name="movie-delete"
    ),
    path("movies/<int:pk>/review/", views.review_movie, name="movie-review"),
    path("reviews/", views.unapproved_reviews, name="unapproved-reviews"),
    path("reviews/<int:pk>/approve/", views.approve_review, name="review-approve"),
    path("directors/", views.get_director_list, name="director-list"),
    path("directors/add/", views.add_director, name="director-add"),
    path("directors/<int:pk>/", views.get_director_detail, name="director-detail"),
    path("directors/<int:pk>/edit/", views.edit_director, name="director-edit"),
    path("directors/<int:pk>/delete/", views.delete_director, name="director-delete"),
]

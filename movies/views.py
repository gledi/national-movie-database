from django.shortcuts import render

from movies.models import Movie


def get_movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies/movie_list.html", context={
        "movies": movies,
    })


def add_movie(request):
    return render(request, "movies/movie_add.html", context={
        
    })
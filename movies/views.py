from http.client import INTERNAL_SERVER_ERROR
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Director, Movie
from movies.forms import MovieForm, MovieModelForm


def get_movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies/movie_list.html", context={
        "movies": movies,
    })


def get_movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk) # select * from movies where id = ?
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
    return render(request, "movies/movie_detail.html", context={
        "movie": movie
    })


def add_movie_old(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = Movie(**form.cleaned_data)
            movie.save()
            # return HttpResponseRedirect(
            #     reverse("movie-detail", kwargs={"pk": movie.pk})
            # )
            # return redirect("movie-detail", pk=movie.pk, permanent=False)
            return redirect(movie, permanent=False)
    else:
        form = MovieForm()
    return render(request, "movies/movie_add.html", context={
        "form": form,
    })


def add_movie(request):
    if request.method == "POST":
        form = MovieModelForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect(movie, permanent=False)
    else:
        form = MovieModelForm()
    return render(request, "movies/movie_form.html", context={
        "form": form,
    })


def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        form = MovieModelForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect(movie)
    else:
        form = MovieModelForm(instance=movie)
    return render(request, "movies/movie_form.html", context={
        "form": form,
        "movie": movie,
    })


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        movie.delete()
        return redirect("movie-list")
    return render(request, "movies/movie_delete.html", context={
        "movie": movie
    })

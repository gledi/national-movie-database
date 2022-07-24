from http.client import INTERNAL_SERVER_ERROR
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Director, Movie
from movies.forms import DirectorForm, MovieForm, MovieModelForm


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


def get_director_list(request):
    directors = Director.objects.all()
    return render(request, "movies/director_list.html", context={
        "directors": directors
    })


def add_director(request):
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            director = form.save()
            return redirect("director-detail", pk=director.pk)
    else:
        form = DirectorForm()
    return render(request, "movies/director_form.html", context={
        "form": form
    })


def get_director_detail(request, pk):
    director = get_object_or_404(Director, pk=pk)
    return render(request, "movies/director_detail.html", context={
        "director": director
    })


# def edit_director(request, pk):
#     director = get_object_or_404(Director, pk=pk)
#     if request.method == "POST":
#         form = DirectorForm(request.POST, request.FILES, instance=director)
#         if form.is_valid():
#             director = form.save()
#             return redirect("director-detail", pk=director.pk)
#     else:
#         form = DirectorForm(instance=director)
#     return render(request, "movies/director_form.html", context={
#         "director": director,
#         "form": form
#     })


def delete_director(request, pk):
    director = get_object_or_404(Director, pk=pk)
    if request.method == "POST":
        director.delete()
        return redirect("director-list")
    return render(request, "movies/director_delete.html", context={
        "director": director
    })


def edit_obj(klass, form_class, context_object_name="obj"):
    def view(request, pk):
        obj = get_object_or_404(klass, pk=pk)
        if request.method == "POST":
            form = form_class(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                obj = form.save()
                return redirect(f"{klass._meta.model_name}-detail", pk=obj.pk)
        else:
            form = form_class(instance=obj)
        return render(request, f"{klass._meta.app_label}/{klass._meta.model_name}_form.html", context={
            "obj": obj,
            "form": form
        })

    return view

edit_director = edit_obj(Director, DirectorForm)

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from movies.models import Director, Movie


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


def add_movie(request):
    directors = Director.objects.all()
    if request.method == "POST":
        movie = Movie(
            title=request.POST["title"],
            plot=request.POST["plot"],
            runtime=int(request.POST["runtime"]),
            year=int(request.POST["year"]),
            director_id=int(request.POST["director_id"]),
            rating=request.POST["rating"],
        )
        movie.save()
        # return HttpResponseRedirect(
        #     reverse("movie-detail", kwargs={"pk": movie.pk})
        # )
        # return redirect("movie-detail", pk=movie.pk, permanent=False)
        return redirect(movie, permanent=False)
    return render(request, "movies/movie_add.html", context={
        "directors": directors
    })

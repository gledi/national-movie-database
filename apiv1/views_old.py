import json

from django.shortcuts import get_object_or_404
from django.http import HttpRequest, JsonResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt

from movies.models import Movie
from .serializers import MovieSerializer, MovieModelSerializer


@csrf_exempt
def get_movie_list(request: HttpRequest):
    if request.method == "GET":
        page_num = int(request.GET.get("page", "1"))
        movies = Movie.objects.order_by('-pk').all()
        paginator = Paginator(movies, per_page=2)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            raise Http404("No more movies")
        ms = MovieModelSerializer(page.object_list, many=True)
        return JsonResponse({"items": ms.data, "total": paginator.count, "page": page.number})
    elif request.method == "POST":
        ms = MovieModelSerializer(data=json.loads(request.body))
        if ms.is_valid():
            movie = Movie(**ms.data, director_id=1)
            movie.save()
            return JsonResponse({"movie": ms.data}, status=201)
        else:
            return JsonResponse(ms.errors, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def get_movie_details(request, pk):
    if request.method == "GET":
        movie = get_object_or_404(Movie, pk=pk)
        ms = MovieModelSerializer(movie)
        return JsonResponse(ms.data)
    elif request.method == "PUT" or request.method == "PATCH":
        ...
        # update
    elif request.method == "DELETE":
        ...
        # remove/delete movie
    else:
        ...
        # method not allowed

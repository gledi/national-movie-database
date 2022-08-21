from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from movies.models import Movie
from .serializers import MovieModelSerializer

class MovieListCreateView(APIView):
    def get(self, request: Request, format=None) -> Response:
        page_num = int(request.GET.get("page", "1"))
        movies = Movie.objects.order_by('-pk').all()
        paginator = Paginator(movies, per_page=2)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            raise Http404("No more movies")
        ms = MovieModelSerializer(page.object_list, many=True)
        return Response({"items": ms.data, "total": paginator.count, "page": page.number})

    def post(self, request: Request, format=None) -> Response:
        ms = MovieModelSerializer(data=request.data)
        if ms.is_valid():
            movie = ms.save(director_id=1)
            return Response(ms.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailUpdateDeleteView(APIView):
    def get(self, request, pk, format=None):
        movie = get_object_or_404(Movie, pk=pk)
        ms = MovieModelSerializer(movie)
        return Response(ms.data)

    def _update(self, request, pk, partial=False):
        movie = get_object_or_404(Movie, pk=pk)
        ms = MovieModelSerializer(movie, data=request.data, partial=partial)
        if ms.is_valid():
            ms.save()
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        return self._update(request, pk)

    def patch(self, request, pk, format=None):
        return self._update(request, pk, partial=True)

    def delete(self, request, pk, format=None):
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

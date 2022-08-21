from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from movies.models import Movie
from .serializers import MovieModelSerializer


class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.order_by('-pk').all()
    serializer_class = MovieModelSerializer
    pagination_class = PageNumberPagination


class MovieDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer

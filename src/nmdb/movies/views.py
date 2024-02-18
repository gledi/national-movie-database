from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import Avg, F, Prefetch
from django.db.models.functions import Round
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.http import require_POST

from nmdb.photos.models import Photo

from .forms import MovieForm, ReviewForm
from .models import Movie, Review, Role


class MovieListView(generic.ListView):
    context_object_name = "movies"
    paginate_by = 6

    def get_queryset(self):
        qs = (
            Movie.objects.prefetch_related(
                Prefetch("photos", Photo.objects.filter(is_primary=True).all())
            )
            .filter(photos__is_primary=True)
            .annotate(caption=F("photos__caption"))
            .annotate(avgrate=Round(Avg("reviews__rating"), precision=1))
        )

        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            vector = SearchVector("title") + SearchVector("plot")
            query = SearchQuery(search_query)
            headline = SearchHeadline(
                "plot",
                query,
                start_sel="<mark>",
                stop_sel="</mark>",
            )

            qs = (
                qs.annotate(search=vector, rank=SearchRank(vector, query))
                .annotate(headline=headline)
                .filter(search=query)
                .order_by("-rank")
                .all()
            )
        else:
            qs = qs.order_by("-created_at").all()

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)

        page_number = int(self.request.GET.get(self.page_kwarg, "1"))
        paginator = context_data["paginator"]
        pages = paginator.get_elided_page_range(
            number=page_number,
            on_each_side=2,
        )

        search_query = self.request.GET.get("q", "").strip()

        context_data.update({"pages": pages, "search_query": search_query})
        return context_data


class MovieDetailView(generic.DetailView):
    context_object_name = "movie"

    def get_queryset(self):
        return Movie.objects.select_related("director").prefetch_related("photos").all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        movie = context_data[self.context_object_name]

        avg_rating = Review.objects.filter(movie=movie).aggregate(
            avgrating=Round(Avg("rating"), precision=1)
        )

        cast = (
            Role.objects.select_related("actor")
            .prefetch_related(
                Prefetch("actor__photos", Photo.objects.filter(is_primary=True).all())
            )
            .filter(movie=movie)
            .all()
        )

        user_rating = {"rating": None}
        if self.request.user.is_authenticated:
            user_rating["rating"] = (
                Review.objects.filter(movie=movie, user=self.request.user)
                .values_list("rating", flat=True)
                .first()
            )

        context_data.update({"cast": cast, **avg_rating, **user_rating})
        return context_data


class MovieCreateView(generic.CreateView):
    model = Movie
    form_class = MovieForm


class MovieUpdateView(generic.UpdateView):
    model = Movie
    form_class = MovieForm


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy("movies:movie-list")


@login_required
@require_POST
def review_movie(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(Movie, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review, created = Review.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"rating": form.cleaned_data["rating"]},
        )
        message = _("Thank you for updating your review.")
        if created:
            message = _("Thank you for your review.")
        current_rating = Review.objects.filter(movie=movie).aggregate(
            rating=Round(Avg("rating"), precision=1)
        )
        return JsonResponse({"detail": message, **current_rating})

    return JsonResponse(
        {
            "detail": _("Could not rate this movie"),
            "errors": form.errors,
        },
        status=400,
    )

import copy
from typing import Any
from urllib.parse import urlencode

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from nmdb.photos.models import Photo

from .filters import PostFilter
from .forms import PostForm
from .models import Post


class PostListView(FilterView):
    queryset = (
        Post.objects.select_related("author")
        .prefetch_related(Prefetch("photos", Photo.objects.filter(is_primary=True)))
        .filter(is_published=True)
        .order_by("-published_on")
        .all()
    )
    context_object_name = "posts"
    paginate_by = 5
    filterset_class = PostFilter
    template_name = "news/post_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        page_number = int(self.request.GET.get(self.page_kwarg, "1"))
        paginator = context["paginator"]
        pages = paginator.get_elided_page_range(
            number=page_number,
            on_each_side=2,
        )

        queryparams = copy.copy(self.request.GET)
        queryparams.pop("page", None)

        context.update({"pages": pages, "queryparams": urlencode(queryparams)})

        return context


class PostDetailView(generic.DetailView):
    queryset = (
        Post.objects.select_related("author")
        .prefetch_related("photos")
        .filter(is_published=True)
        .all()
    )


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("news:post-list")

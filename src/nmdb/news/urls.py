from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("<slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("add/", views.PostCreateView.as_view(), name="post-add"),
    path("<slug>/edit/", views.PostUpdateView.as_view(), name="post-edit"),
    path("<slug>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
]

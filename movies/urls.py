from django.urls import path

from . import views


urlpatterns = [
    path("actors/", views.get_actor_list, name="actor-list"),
    path("actors/<int:id>/", views.get_actor_detail, name="actor-detail"),
]

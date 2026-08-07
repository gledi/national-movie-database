from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http import HttpRequest

from nmdb.photos.models import Photo

from .models import Post


class PhotosInline(GenericTabularInline):
    model = Photo


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_on")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}  # noqa: RUF012
    inlines = (PhotosInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Post]:
        return super().get_queryset(request).select_related("author")

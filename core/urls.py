from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("", include("movies.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/", include("registration.backends.default.urls")),
    path("api/v1/", include("apiv1.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

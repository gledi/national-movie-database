from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("nmdb.pages.urls")),
    path("accounts/", include("registration.backends.default.urls")),
    path("accounts/", include("nmdb.users.urls")),
    path("movies/", include("nmdb.movies.urls")),
    path("news/", include("nmdb.news.urls")),
    # path("shop/", include("nmdb.shop.urls")),
    path("api/v1/", include("nmdb.apiv1.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

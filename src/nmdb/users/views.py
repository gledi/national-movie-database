from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Profile


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(
        Profile.objects.select_related("user").prefetch_related("photos"),
        user=request.user,
    )
    picture = profile.photos.filter(is_primary=True).first()
    return render(
        request,
        "registration/profile.html",
        context={"profile": profile, "picture": picture},
    )

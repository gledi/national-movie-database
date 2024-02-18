from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def signin_required(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Only authenticated users can add movies!")
            return redirect(settings.LOGIN_REDIRECT_URL)
        return view_func(request, *args, **kwargs)

    return _wrapper

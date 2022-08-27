from typing import Any

from django.http import HttpRequest
from django.conf import settings

from pages.models import Setting


def get_site_info_old(request: HttpRequest) -> dict[str, Any]:
    return {
        "page_title": settings.PAGE_TITLE,
        "copyright_year": settings.COPYRIGHT_YEAR,
        "copyright_company": settings.COPYRIGHT_COMPANY,
    }


def get_site_info(request):
    return {s.key: s.value for s in Setting.objects.all()}

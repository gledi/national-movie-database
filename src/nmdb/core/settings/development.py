from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS.extend(["django_extensions", "debug_toolbar"])

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ["127.0.0.1"]

SHELL_PLUS_IMPORTS = [
    "from django.core.files.images import ImageFile",
    "from django.contrib.staticfiles import finders",
    "from django.contrib.staticfiles.storage import staticfiles_storage",
    "import os",
    "import io",
    "import sys",
    "import csv",
    "import datetime as dt",
    "import random",
    "from decimal import Decimal",
    "import requests",
    "from faker import Faker",
]

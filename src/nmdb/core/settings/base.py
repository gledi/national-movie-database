from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environs import Env

env = Env()
env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent

SECRET_KEY = env("SECRET_KEY", "SuperSecret")

DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", [])


INSTALLED_APPS = [
    "django.contrib.sites",
    "registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "imagekit",
    "taggit",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_filters",
    "rest_framework",
    "mptt",
    "nmdb.pages",
    "nmdb.photos",
    "nmdb.users",
    "nmdb.movies",
    "nmdb.news",
    # "shop",
    "nmdb.apiv1",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nmdb.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "shop.context_processors.cart_total_amount",
            ],
        },
    },
]

WSGI_APPLICATION = "nmdb.core.wsgi.application"


_default_dburl = (BASE_DIR / "db.sqlite3").as_uri().replace("file:/", "sqlite:/")
DATABASES = {"default": env.dj_db_url("DATABASE_URL", default=_default_dburl)}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

USE_I18N = True
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en-us", _("English (US)")),
    ("sq-al", _("Albanian")),
]
LOCALE_PATHS = [BASE_DIR / "locales"]


USE_TZ = True
TIME_ZONE = "UTC"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = ROOT_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = ROOT_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"


CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap5",)
CRISPY_TEMPLATE_PACK = "bootstrap5"


LOGIN_URL = "auth_login"
LOGOUT_URL = "auth_logout"
LOGIN_REDIRECT_URL = "users:profile"
LOGOUT_REDIRECT_URL = "pages:home"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SITE_ID = 1

# Registration
REGISTRATION_OPEN = True
REGISTRATION_FORM = "nmdb.users.forms.RegistrationForm"
ACCOUNT_ACTIVATION_DAYS = 7
INCLUDE_AUTH_URLS = True


# Stripe payments
STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = env.str("STRIPE_SECRET_KEY", "")

CART_SESSION_ID = "cart"

USER_AVATAR_SIZE = (800, 600)
USER_AVATAR_FONT_SIZE = 256
USER_AVATAR_FONT_VARIANTS = {
    "light": "fonts/OpenSans/OpenSans-Light.ttf",
    "regular": "fonts/OpenSans/OpenSans-Regular.ttf",
    "medium": "fonts/OpenSans/OpenSans-Medium.ttf",
    "semibold": "fonts/OpenSans/OpenSans-SemiBold.ttf",
    "bold": "fonts/OpenSans/OpenSans-Bold.ttf",
}

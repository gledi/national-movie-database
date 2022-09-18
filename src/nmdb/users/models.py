from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from nmdb.photos.models import Photo

from .managers import UserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    name = models.CharField(_("name"), max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    nickname = models.CharField(_("nickname"), max_length=32, null=True, blank=True)
    telno = models.CharField(
        _("telephone number"),
        max_length=32,
        null=True,
        blank=True,
    )
    address = models.TextField(_("address"), null=True, blank=True)
    bio = models.TextField(_("bio"), null=True, blank=True)
    photos = GenericRelation(Photo, related_query_name="profile")

    class Meta:
        db_table = "profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self) -> str:
        return self.nickname

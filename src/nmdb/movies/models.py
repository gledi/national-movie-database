from __future__ import annotations

import secrets

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models, transaction
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from nmdb.core.models import BaseModel
from nmdb.core.utils import markdown
from nmdb.photos.models import Photo

_poster_sizes = frozenset(
    [
        "xl",
        "lg",
        "md",
        "sm",
        "xs",
        "thumb",
    ]
)


def generate_slug(movie: Movie, new_slug: str | None = None) -> str:
    if new_slug is not None and new_slug.strip():
        slug = new_slug
    else:
        slug = slugify(movie.title)

    slug_exists = movie.__class__.objects.filter(slug=slug).exists()
    if slug_exists:
        rand = secrets.token_hex(2)
        new_slug = f"{slug}-{rand}"
        return generate_slug(movie, new_slug=new_slug)

    return slug


class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Person(BaseModel):
    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("Person's full name"),
    )
    birthdate = models.DateField(_("birthdate"), null=True, blank=True)
    bio = models.TextField(_("bio"), null=True, blank=True)
    photos = GenericRelation(Photo, related_query_name="person")

    class Meta:
        db_table = "people"
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __str__(self) -> str:
        return f"{self.name}"

    @cached_property
    def bio_html(self) -> str:
        if self.bio is None:
            return "N/A"
        return markdown.parse(self.bio)

    @cached_property
    def mug(self) -> Photo | None:
        return self.photos.filter(is_primary=True).first()

    def _get_default_pic_url(self, size=None) -> str:
        name = "mug"
        if size in _poster_sizes:
            name = f"{name}_{size}"
        path = f"images/people/{name}.png"
        return staticfiles_storage.url(path)

    def get_pic_url(self, size=None):
        if self.mug is None:
            return self._get_default_pic_url(size=size)

        if size is None or size not in _poster_sizes:
            size = "photo"

        photo = getattr(self.mug, size, self.mug.photo)

        return photo.url


class Movie(BaseModel):
    class Ratings(models.TextChoices):
        G = "G", _("G: General Audiences")
        PG = "PG", _("PG: Parental Guidance Suggesteds")
        PG13 = "PG-13", _("PG-13: Parents Strongly Cautioned")
        R = "R", _("R - Restricted")
        NC17 = "NC-17", _("NC-17: Adults Only")

    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    year = models.IntegerField(_("year"), help_text=_("Movie's release year"))
    plot = models.TextField(_("plot"), null=True, blank=True)
    runtime = models.IntegerField(
        _("runtime"),
        null=True,
        blank=True,
        help_text=_("Movie runtime in minutes"),
    )
    mpaa_rating = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        choices=Ratings.choices,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name=_("genre"),
        null=True,
        blank=True,
        related_name="movies",
        on_delete=models.SET_NULL,
    )
    director = models.ForeignKey(
        Person,
        verbose_name=_("director"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movies_directed",
    )
    actors = models.ManyToManyField(Person, through="Role", related_name="movies")
    photos = GenericRelation(Photo, related_query_name="movie")
    tags = TaggableManager()

    class Meta:
        db_table = "movies"
        verbose_name = _("movie")
        verbose_name_plural = _("movies")
        constraints = [
            models.CheckConstraint(check=Q(year__gte=1900), name="chk_movies_year"),
            models.CheckConstraint(
                check=Q(runtime__gte=20) & Q(runtime__lte=480),
                name="chk_movies_runtime",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"

    def get_absolute_url(self) -> str:
        return reverse("movies:movie-detail", kwargs={"pk": self.pk})

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self)
        return super().save(*args, **kwargs)

    @cached_property
    def poster(self) -> Photo | None:
        return self.photos.filter(is_primary=True).first()

    def _get_default_pic_url(self, size=None) -> str:
        name = "poster"
        if size in _poster_sizes:
            name = f"{name}_{size}"
        path = f"images/movies/{name}.png"
        return staticfiles_storage.url(path)

    def get_pic_url(self, size=None):
        if self.poster is None:
            return self._get_default_pic_url(size=size)

        if size is None or size not in _poster_sizes:
            size = "photo"

        photo = getattr(self.poster, size, self.poster.photo)

        return photo.url

    @cached_property
    def plot_html(self) -> str:
        if self.plot is None:
            return "N/A"
        return markdown.parse(self.plot)


class Role(models.Model):
    movie = models.ForeignKey(
        Movie,
        verbose_name=_("movie"),
        related_name="roles",
        on_delete=models.CASCADE,
    )
    actor = models.ForeignKey(
        Person,
        verbose_name=_("actor"),
        related_name="roles",
        on_delete=models.CASCADE,
    )
    role = models.CharField(_("role"), max_length=255)

    class Meta:
        db_table = "roles"
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self) -> str:
        return self.role


class Review(BaseModel):
    movie = models.ForeignKey(
        Movie,
        verbose_name=_("movie"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(_("rating"))
    content = models.TextField(_("content"), null=True, blank=True)
    is_approved = models.BooleanField(_("is approved"), default=False)

    class Meta:
        db_table = "reviews"
        verbose_name = _("review")
        verbose_name_plural = _("reviews")
        permissions = [
            ("approve_review", "Can approve review"),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5), name="chk_reviews_rating"
            ),
            models.UniqueConstraint(
                fields=["user", "movie"], name="uq_reviews_user_movie"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user!r} reviewd {self.movie!r} {self.rating} stars"

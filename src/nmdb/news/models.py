from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from nmdb.core.models import BaseModel
from nmdb.core.utils import markdown
from nmdb.photos.models import Photo


class Post(BaseModel):
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    body = models.TextField(_("body"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        null=True,
        blank=True,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    is_published = models.BooleanField(_("is published?"), default=False)
    published_on = models.DateTimeField(_("published on"), null=True, blank=True)
    photos = GenericRelation(Photo, related_query_name="post")

    class Meta:
        db_table = "posts"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.slug is None:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @cached_property
    def body_html(self) -> str:
        return markdown.parse(self.body)

    @transaction.atomic
    def publish(self) -> None:
        self.is_published = True
        self.published_on = timezone.now()
        self.save()

    def get_absolute_url(self) -> str:
        return reverse("news:post-detail", kwargs={"pk": self.pk})

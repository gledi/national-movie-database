from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Thumbnail

from nmdb.core.models import BaseModel


class Photo(BaseModel):
    photo = models.ImageField(_("photo"), upload_to="photos/%Y/%m/%d")
    caption = models.CharField(_("caption"), max_length=255, null=True, blank=True)
    is_primary = models.BooleanField(_("is primary"), default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey()

    xl = ImageSpecField(
        source="photo", format="PNG", processors=[ResizeToFill(600, 800)]
    )
    lg = ImageSpecField(
        source="photo", format="PNG", processors=[ResizeToFill(480, 640)]
    )
    md = ImageSpecField(
        source="photo", format="PNG", processors=[ResizeToFill(360, 480)]
    )
    sm = ImageSpecField(
        source="photo", format="PNG", processors=[ResizeToFill(240, 320)]
    )
    xs = ImageSpecField(
        source="photo", format="PNG", processors=[ResizeToFill(120, 160)]
    )
    thumb = ImageSpecField(source="photo", format="PNG", processors=[Thumbnail(96, 96)])

    class Meta:
        db_table = "photos"
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __str__(self) -> str:
        if self.caption is None or not self.caption.strip():
            return self.photo.name
        return self.caption

    @transaction.atomic
    def save(self, *args, **kwargs):
        photos = self.__class__.objects.filter(
            Q(content_type=self.content_type)
            & Q(object_id=self.object_id)
            & Q(is_primary=True)
            & ~Q(pk=self.pk)
        ).all()
        self.is_primary = self.is_primary or (not photos.exists())
        if self.is_primary:
            photos.update(is_primary=False)
        super().save(*args, **kwargs)

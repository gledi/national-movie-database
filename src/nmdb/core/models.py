from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("created at"), editable=False, default=timezone.now
    )
    updated_at = models.DateTimeField(
        _("updated at"), editable=False, default=timezone.now
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

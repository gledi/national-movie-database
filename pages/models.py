from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=32)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        db_table = "settings"

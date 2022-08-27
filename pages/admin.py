from django.contrib import admin

from pages.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass

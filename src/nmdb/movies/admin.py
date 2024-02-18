import datetime as dt

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Genre, Movie, Person

admin.site.register(Genre, MPTTModelAdmin)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "runtime", "mpaa_rating"]
    list_filter = ["mpaa_rating"]
    list_editable = ["year", "runtime"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name", "birthday"]

    @admin.display(empty_value="-")
    def birthday(self, obj):
        today = dt.date.today()
        if obj.birthdate.day == today.day and obj.birthdate.month == today.month:
            return "Happy Birthday"
        return obj.birthdate

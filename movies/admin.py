import datetime as dt
from django.contrib import admin

from movies.models import Movie, Actor, Director


admin.site.register(Actor)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'runtime', 'rating']
    list_filter = ['rating']
    list_editable = ['year', 'runtime']


admin.site.register(Movie, MovieAdmin)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'birthday']

    @admin.display(empty_value='-')
    def birthday(self, obj):
        today = dt.date.today()
        if obj.birthdate.day == today.day and obj.birthdate.month == today.month:
            return 'Happy Birthday'
        return obj.birthdate

import datetime as dt
from django import forms

from .models import Director, Movie, Review


def _get_directors():
    return [("", "-- Director --")] + [
        (director.pk, str(director)) for director in Director.objects.all()
    ]


def _to_director(val):
    pk = int(val)
    return Director.objects.get(pk=pk)


RATINGS = [
    ("", "-- Rating --"),
    ("G", "G - General Audiences"),
    ("PG", "PG - Parental Guidance Suggesteds"),
    ("PG-13", "PG-13 - Parents Strongly Cautioned"),
    ("R", "R - Restricted"),
    ("NC-17", "NC-17 – Adults Only"),
]


class MovieForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    year = forms.IntegerField(min_value=1900, required=True)
    runtime = forms.IntegerField(min_value=10, max_value=500, required=True)
    plot = forms.CharField(widget=forms.Textarea, required=False)
    rating = forms.ChoiceField(required=True, choices=RATINGS)
    director = forms.TypedChoiceField(
        required=True, coerce=_to_director, choices=_get_directors
    )


class MovieModelForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "year",
            "runtime",
            "plot",
            "rating",
            "director",
        ]

    def clean_year(self):
        today = dt.date.today()
        year = self.cleaned_data["year"]
        if year < 1900 or year > today.year + 1:
            raise forms.ValidationError("Invalid movie release year")
        return year

    def clean_runtime(self):
        runtime = self.cleaned_data["runtime"]
        if 20 <= runtime <= 600:
            return runtime
        raise forms.ValidationError("Movies last between 20 and 600 minutes only")


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "rating",
            "content",
        ]

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must bee between 1 and 5")
        return rating

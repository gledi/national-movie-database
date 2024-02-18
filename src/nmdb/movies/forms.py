import datetime as dt

from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "year",
            "runtime",
            "plot",
            "mpaa_rating",
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


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)
    content = forms.CharField(required=False, widget=forms.Textarea)

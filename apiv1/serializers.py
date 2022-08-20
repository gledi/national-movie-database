from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    year = serializers.IntegerField()
    runtime = serializers.IntegerField()
    plot = serializers.CharField()
    rating = serializers.CharField()


class MovieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "year",
            "runtime",
            "plot",
            "rating",
        ]

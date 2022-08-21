from rest_framework import serializers

from movies.models import Movie, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "content"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating should be between 1 and 5")
        return value

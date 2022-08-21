import re

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from movies.models import Director


User = get_user_model()

class AddMovieTest(TestCase):
    def setUp(self):
        self.url = reverse("movie-add")
        self.re_movie_url = re.compile(r'^/movies/\d+/$')
        self.user = User.objects.create_user(
            "test",
            email="test@example.com",
            password="SuperS3cret",
        )
        self.director = Director.objects.create(
            first_name="Steven",
            last_name="Spielberg",
        )
        return super().setUp()

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            "title": "Test",
            "year": 2000,
            "runtime": 100,
            "plot": "something happens",
            "rating": "G",
            "director": self.director.pk
        })
        self.assertRegexpMatches(response.headers["Location"], self.re_movie_url)
        self.assertEqual(response.status_code, 302)

    def test_not_allow_invalid_movies(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            "title": "Test",
            "year": 1800,
            "runtime": 100,
            "plot": "something happens",
            "rating": "G",
            "director": self.director.pk
        })
        self.assertContains(response, "Invalid movie release year")

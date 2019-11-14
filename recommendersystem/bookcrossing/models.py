from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import requests
from django.conf import settings


class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_yr = models.CharField(max_length=10)
    publisher = models.CharField(max_length=50)
    image_url_s = models.URLField()
    image_url_m = models.URLField()
    image_url_l = models.URLField()

    def __str__(self):
        return f'"{self.title}" by {self.author}'

    def get_fields_for_display(self):
        display = {
            "ISBN": self.isbn,
            "Title": self.title,
            "Author": self.author,
            "Publication Year": self.publication_yr
        }
        return display

    def get_image_for_display(self):
        return self.image_url_l

    class Meta:
        ordering = ["pk"]


class User(models.Model):
    user_id = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    age = models.CharField(max_length=3)

    def __str__(self):
        location = self.location.split(",")[-1].upper()
        return f"User: {self.user_id} Location: {location}\tAge:{self.age}"

    def __repr__(self):
        return self.user_id

    def get_fields_for_display(self):
        display = {
            "User ID": self.user_id,
            "Location": self.location.split(',')[-1],
            "Age": self.age,
        }
        return display

    def get_ratings_for_display(self):
        response = requests.get(
            settings.DEFAULT_ORIGIN + reverse("api-rating-list"),
            params={"user_id": self.user_id})
        json_response = response.json()
        ratings = []
        for result in json_response["results"]:
            ratings.append((result["rating"], result["isbn_url"]))
        return ratings

    class Meta:
        ordering = ["pk"]


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    isbn = models.ForeignKey(Book, on_delete=models.PROTECT)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Book {self.isbn} User {self.user_id}: {self.rating}"

    def get_fields_for_display(self):
        display = {
            "User ID": self.user_id.id,
            "ISBN": self.isbn.isbn,
            "Rating": self.rating,

        }
        return display

    def get_image_for_display(self):
        return self.isbn.image_url_l

    class Meta:
        ordering = ["pk"]

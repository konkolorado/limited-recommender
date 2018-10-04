from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
        return f"{self.title} by {self.author}, {self.publication_yr}"

    class Meta:
        ordering = ["title"]


class User(models.Model):
    user_id = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    age = models.CharField(max_length=3)

    def __str__(self):
        return f"User: {self.user_id} Location:{self.location} Age:{self.age}"

    def __repr__(self):
        return self.user_id

    class Meta:
        ordering = ["user_id"]


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    isbn = models.ForeignKey(Book, on_delete=models.PROTECT)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Book {self.isbn}\tUser {self.user_id}: {self.rating}"

    class Meta:
        ordering = ["user_id"]

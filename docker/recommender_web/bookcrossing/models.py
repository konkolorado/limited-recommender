from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_yr = models.CharField(max_length=10)
    publisher = models.CharField(max_length=50)
    image_url_s = models.URLField()
    image_url_m = models.URLField()
    image_url_l = models.URLField()

class User(models.Model):
    user_id = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()

class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    isbn = models.ForeignKey(Book, on_delete=models.PROTECT)
    rating = models.SmallIntegerField()

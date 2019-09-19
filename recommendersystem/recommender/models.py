from django.db import models
from bookcrossing.models import Book


class Similarity(models.Model):
    rated = models.ForeignKey(Book, on_delete=models.PROTECT,
                              related_name='predictive_item')
    target = models.ForeignKey(Book, on_delete=models.PROTECT,
                               related_name='recommended_item')
    similarity_score = models.DecimalField(max_digits=15, decimal_places=14)

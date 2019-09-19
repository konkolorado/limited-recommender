from django.core.management.base import BaseCommand
from bookcrossing.models import User, Book, Rating
from recommender.models import Similarity
import numpy

from collections import defaultdict


class Command(BaseCommand):
    help = 'Bootstraps the initial item-similarity matrix'
    """
    For each item in product catalog, I1
        For each customer C who purchased I1
            For each item I2 purchased by customer C
                Record that a customer purchased I1 and I2
        For each item I2 Compute the similarity between I1 and I2
    """

    def __init__(self):
        self.added_counter = 0
        self.n_users = User.objects.all().count()

    def calc_cosine_similarity(self, a, b):
        """ Computes the cosine similarity between two 1-dimensional lists """
        return numpy.dot(a, b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))

    def ddict_callable(self):
        """
        A callable that can be supplied to defaultdicts to initialize keys
        with a list of zeroes of length # of Users
        """
        return list([0]) * self.n_users

    def compute_similarities(self, item, co_rated_items, precision=14):
        """
        Computes cosine similarity scores between item and all other items
        in co_rated_items dictionary
        """
        similarities = dict()
        for co_rated in co_rated_items:
            if co_rated == item:
                continue
            score = self.calc_cosine_similarity(co_rated_items[item],
                                                co_rated_items[co_rated])
            similarities[co_rated] = round(score, precision)
        return similarities

    def commit_similarities(self, item, similarities):
        """
        Takes an object identifier "item" and a dict of similarities where each
        key is another object identifier and the value is the similarity
        between the two items
        """
        for similar_item_isbn in similarities:
            _, new = Similarity.objects.get_or_create(
                rated=Book.objects.get(isbn=item),
                target=Book.objects.get(isbn=similar_item_isbn),
                similarity_score=similarities[similar_item_isbn])
            if new:
                self.added_counter += 1

    def handle(self, *args, **options):
        # For each item in catalog
        for book in Book.objects.all():
            co_rated_items = defaultdict(self.ddict_callable)

            # For each customer c who purchased item
            for rating in Rating.objects.filter(isbn__id=book.id):
                # Record c rated book and other_rated_book, part 1
                co_rated_items[book.isbn][rating.user_id.id-1] = 1

                # For every other item purchased by customer c
                for co_rated_book in Rating.objects.filter(
                        user_id__id=rating.user_id.id).exclude(
                        isbn__id=book.id):

                    # Record c rated book and other_rated_book, part 2
                    co_rated_items[co_rated_book.isbn.isbn][rating.user_id.id-1] = 1

            # For each item bought along with item, compute similarity
            sims = self.compute_similarities(book.isbn, co_rated_items)

            # Store item to item similarities
            self.commit_similarities(book.isbn, sims)

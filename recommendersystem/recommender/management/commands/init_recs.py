from django.core.management.base import BaseCommand
from bookcrossing.models import User, Book, Rating
from recommender.models import Similarity
import numpy

from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


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
        self.new_counter = 0
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

    def compute_similarities(self, source, item_to_item, precision=14):
        """
        Computes cosine similarity scores between item and all other items
        in co_rated_items dictionary
        """
        similarities = dict()
        for other_item in item_to_item:
            if other_item == source:
                continue
            score = self.calc_cosine_similarity(item_to_item[source],
                                                item_to_item[other_item])
            similarities[other_item] = round(score, precision)
        return similarities

    def commit_similarities(self, item, similarities):
        """
        Takes an object identifier "item" and a dict of similarities where each
        key is another object identifier and the value is the similarity
        between the two items
        """
        for similar_item_isbn in similarities:
            _, new = Similarity.objects.get_or_create(
                source=Book.objects.get(isbn=item),
                target=Book.objects.get(isbn=similar_item_isbn),
                similarity_score=similarities[similar_item_isbn])
            self.added_counter += 1
            if new:
                self.new_counter += 1

    def handle(self, *args, **options):
        # For each item in catalog
        for book in Book.objects.all():
            item_to_item = defaultdict(self.ddict_callable)

            # For each customer c who purchased item
            for rating in Rating.objects.filter(isbn__id=book.id):
                # Record c rated book and other_rated_book, part 1
                item_to_item[book.isbn][rating.user_id.id-1] = 1

                # For every other item purchased by customer c
                for rated_book in Rating.objects.filter(
                        user_id__id=rating.user_id.id).exclude(
                        isbn__id=book.id):

                    # Record c rated book and other_rated_book, part 2
                    item_to_item[rated_book.isbn.isbn][rating.user_id.id-1] = 1

            # For each item bought along with item, compute similarity
            sims = self.compute_similarities(book.isbn, item_to_item)

            # Store item to item similarities
            self.commit_similarities(book.isbn, sims)
        logger.info(f"Processed {self.added_counter} similarity scores")
        logger.info(f"Added {self.new_counter} new similarity scores")

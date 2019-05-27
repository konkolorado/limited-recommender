from django.core.management.base import BaseCommand
from bookcrossing.models import User, Book, Rating
import numpy


class Command(BaseCommand):
    help = 'Bootstraps the initial item-similarity matrix'
    """
    For each item in product catalog, I1
        For each customer C who purchased I1
            For each item I2 purchased by customer C
                Record that a customer purchased I1 and I2
        For each item I2 Compute the similarity between I1 and I2
    """

    def calc_cosine_similarity(self, a, b):
        # Computes the cosine similarity between two 1-dimensional lists
        return numpy.dot(a, b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))

    def handle(self, *args, **options):
        books = Book.objects.all()
        n_users = User.objects.all().count()

        for book in books:
            similar_books_collection = dict()
            similar_books_collection[book.title] = [0] * n_users

            # get ratings for book b, store in set A
            ratings_on_book = Rating.objects.filter(isbn__id=book.id)

            # for each user in set A
            for rating in ratings_on_book:
                # Determine what else they rated, store in set B
                rater_id = rating.user_id.id
                users_other_ratings = Rating.objects.filter(
                    user_id__id=rater_id).exclude(isbn__id=book.id)

                # Record somewhere that user bought both items
                for other_rating in users_other_ratings:
                    other_title = other_rating.isbn.title

                    if other_title not in similar_books_collection:
                        similar_books_collection[other_title] = [0] * n_users
                    similar_books_collection[other_title][rater_id-1] = 1
                    similar_books_collection[book.title][rater_id-1] = 1

            for book_title in similar_books_collection:
                if book_title == book.title:
                    continue
                print(self.calc_cosine_similarity(
                    similar_books_collection[book.title],
                    similar_books_collection[book_title]))

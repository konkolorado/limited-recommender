from django.core.management.base import BaseCommand, CommandError
from bookcrossing.models import User, Book, Rating


class Command(BaseCommand):
    help = 'Creates the initial item-similarity matrix'

    """
    For each item in product catalog, I1
        For each customer C who purchased I1
            For each item I2 purchased by customer C
                Record that a customer purchased I1 and I2
        For each item I2 Compute the similarity between I1 and I2
    """

    def handle(self, *args, **options):
        books = Book.objects.all()

        for b in books:
            # get ratings for book b, store in set A
            ratings_on_book = Rating.objects.filter(isbn__id=b.id)
            similar_books = []

            # for each user in set A
            for r in ratings_on_book:
                rater_id = r.user_id.id
                # Determine what else they rated, store in set B
                users_other_ratings = Rating.objects.filter(
                    user_id__id=rater_id).exclude(isbn__id=b.id)

                # Record somewhere that user bought both items
                for other_rating in users_other_ratings:
                    similar_books.append(other_rating.isbn.id)

            # calculate similarity between b.id and ids in similar_books
            # use cosine measure
            # each vector corresponds to an item rather than a
            # customer, and the vector’s M dimensions correspond
            # to customers who have purchased that item.
            #         item1 |  item2 | item 3
            # userA |   X   |    X   |   -
            # userB |   -   |    X   |   -
            # userC |   -   |    -   |   X
            print(b.id, similar_books)

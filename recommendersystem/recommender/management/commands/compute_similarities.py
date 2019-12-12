from django.core.management.base import BaseCommand

from recommender.tasks import compute_similarities


class Command(BaseCommand):
    help = 'Bootstraps the initial item-similarity matrix'
    """
    For each item in product catalog, I1
        For each customer C who purchased I1
            For each item I2 purchased by customer C
                Record that a customer purchased I1 and I2
        For each item I2 Compute the similarity between I1 and I2
    """

    def handle(self, *args, **options):
        compute_similarities.publish()

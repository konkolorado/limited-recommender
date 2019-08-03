from django.core.management.base import BaseCommand

from recommender.tasks import empty_func


class Command(BaseCommand):
    help = 'Launches a python process that uses kombu to produce and ' \
        'publish messages to queues.'

    def handle(self, *args, **options):
        empty_func(2, 10)

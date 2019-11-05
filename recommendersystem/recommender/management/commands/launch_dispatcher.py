from django.core.management.base import BaseCommand
from kombu import Connection, Exchange, Queue

from django.conf import settings

from recommender.queue.worker import Worker


class Command(BaseCommand):
    help = 'Launches a Python process that uses kombu to consume messages ' \
        'from queues.'

    def handle(self, *args, **options):
        # Full kombu documentation at:
        # https://buildmedia.readthedocs.org/media/pdf/kombu/latest/kombu.pdf
        exchange = Exchange("recommendations-exchange", type="direct")
        queues = [Queue(name="recommendations-queue", exchange=exchange,
                        routing_key="new_recommendation")]
        with Connection(settings.BROKER_URL, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

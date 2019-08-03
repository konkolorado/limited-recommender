"""
A decorator implementation that wraps a function and sends it to a Consumer
for execution
"""
from kombu import Connection, Exchange, Queue

from django.conf import settings

import sys

# Function taken from AWX Project
# https://github.com/ansible/awx/blob/devel/awx/main/dispatch/publish.py#L14


def serialize_task(f):
    return '.'.join([f.__module__, f.__name__])


class task(object):
    def __init__(self, exchange, queue,  routing_key):
        """
        The decorated function is not passed to __init__ if there are
        decorator arguments. Arguments must get handled in __call__
        """
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key

    def __call__(self, function):

        # The inner function is required to capture the arguments passed to
        # the decorated function
        def wrapper(*args, **kwargs):

            exchange = Exchange(self.exchange, type="direct")
            queue = Queue(self.queue, exchange=exchange,
                          routing_key=self.routing_key)

            with Connection(settings.BROKER_URL) as conn:
                producer = conn.Producer(serializer='json')
                producer.publish({'function': serialize_task(function),
                                  'args': args,
                                  'kwargs': kwargs},
                                 exchange=exchange,
                                 routing_key='new_recommendation',
                                 declare=[queue],
                                 retry=True)
            print("Published message")
            sys.stdout.flush()

        # Required to allow the task to be called without triggering
        # another message to be published
        wrapper._original = function
        return wrapper

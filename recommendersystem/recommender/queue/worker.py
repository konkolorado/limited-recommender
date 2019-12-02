from kombu.mixins import ConsumerMixin

import importlib


class Worker(ConsumerMixin):
    """
    Full kombu documentation at:
    https://buildmedia.readthedocs.org/media/pdf/kombu/latest/kombu.pdf
    """

    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        callable = self.return_callable(body)
        args = body.get('args', [])
        kwargs = body.get('kwargs', {})

        result = callable(*args, **kwargs)
        #print('Got message: {0}, with result {1}'.format(body, result))
        # sys.stdout.flush()
        message.ack()

    def return_callable(self, body):
        module, task = body['function'].rsplit('.', 1)
        module = importlib.import_module(module)
        callable = getattr(module, task, None)
        return callable.execute

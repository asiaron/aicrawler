"""
worker.py

TODO описание модуля

created by alex in alex as 7/5/20
Проект aicrawler
"""


__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['pavelmstu', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '20200605'

from kombu import Queue, Exchange, Connection, Message
from kombu.mixins import ConsumerProducerMixin
import logging
import argparse


class Worker(ConsumerProducerMixin):
    def __init__(self, connection, in_, out, logger=logging.getLogger()):
        self.connection = connection
        self.in_ = Queue(in_)
        self.out = Exchange(out)
        self.logger = logger

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.in_,
                         on_message=self.handle_message,
                         prefetch_count=10)]

    def handle_message(self, message):
        self.logger.info(msg=f'Got message {message.delivery_tag}')
        try:
            results = self.process_message(message.body)
            for result in results:
                self.producer.publish(
                    body=result,
                    exchange=self.out
                )
            self.logger.info(msg=f'Message {message.delivery_tag} successfully accomplished')
        except Exception as e:
            self.logger.error(msg=e)
        finally:
            message.ack()

    def process_message(self, body: str) -> str:
        raise NotImplementedError

    @classmethod
    def run_from_args(cls, default_in: str, default_out: str):
        parser = argparse.ArgumentParser(
            description='',  # TODO
        )

        parser.add_argument(
            '--in',
            dest='input_queue',
            help='Input RabbitMQ queue',
            default=default_in
        )

        parser.add_argument(
            '--out',
            dest='output_queue',
            help='output RabbitMQ exchange',
            default=default_out
        )

        args = parser.parse_args()
        logger = logging.getLogger('aicrawler')
        logger.setLevel(logging.DEBUG)
        with Connection('amqp://') as connection:
            cls(connection, args.input_queue, args.output_queue, logger=logger).run()
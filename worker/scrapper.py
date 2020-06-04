"""

# TODO

"""

__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['alex', 'pavelmstu']
__copyright__ = 'LGPL v.3'
__status__ = 'Development'
__version__ = '20200602'

import argparse

import configparser
import dataclasses
import logging
from kombu import Connection, Queue, Exchange, Message
from kombu.mixins import ConsumerProducerMixin
from time import sleep
import json

# from core.auto.rss import RssParser

# config = configparser.ConfigParser()
# config.read('./scrapper.ini')
# connection_setting = config['CONNECTION']
# rss_sources = config['RSS_SOURCES']


# ! не убирать
import processing.scrapper.imports


parser = argparse.ArgumentParser(
    description='',  # TODO
)


parser.add_argument(
    '--in',
    dest='input_queue',
    help='Input RabbitMQ queue',
    default='scrapper-in'
)


parser.add_argument(
    '--out',
    dest='output_queue',
    help='output RabbitMQ exchange',
    default='scrapper-out-ex'
)


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

    def handle_message(self, message: Message):
        self.logger.info(msg=f'Got message {message.delivery_tag}')
        try:
            body = json.loads(message.body)
            task = body['task']
            kwargs = body['kwargs']
            func = processing.scrapper.imports._TASKS_ENVIRONMENT[task]
            pages = func(**kwargs)
            for page in pages:
                self.producer.publish(
                    body=page.to_json(),
                    exchange=self.out
                )
            self.logger.info(msg=f'Message {message.delivery_tag} successfully accomplished')
        except Exception as e:
            self.logger.error(msg=e)
        finally:
            message.ack()


def main(input_queue, output_queue):
    logger = logging.getLogger('aicrawler')
    logger.setLevel(logging.DEBUG)
    with Connection('amqp://') as connection:
        Worker(connection, input_queue, output_queue, logger=logger).run()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.input_queue, args.output_queue)
else:
    raise Exception(f"File {__name__} can't be import")

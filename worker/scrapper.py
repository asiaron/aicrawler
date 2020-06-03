"""

# TODO

"""

__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['alex', 'pavelmstu']
__copyright__ = "LGPL v.3"
__status__ = 'Development'
__version__ = '20200602'

import argparse

import configparser
from amqp.connection import Connection
from amqp.basic_message import Message
import logging
from time import sleep

from core.auto.rss import RssParser

config = configparser.ConfigParser()
config.read('./scrapper.ini')
connection_setting = config['CONNECTION']
rss_sources = config['RSS_SOURCES']


# ! не убирать
import processing.scrapper.imports


# TODO
# https://docs.python.org/3/library/argparse.html
#   ИЛИ https://click.palletsprojects.com/en/7.x/
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
    dest='input_queue',
    help='output RabbitMQ exchange',
    default='scrapper-out-ex'
)


# TODO
def main(a, b, c):
    ...


if __name__ == "__main__":
    with Connection(**connection_setting) as connection:
        channel = connection.channel()
        for name, url in rss_sources.items():
            logging.info(f'Getting rss for {name}')
            info_list = RssParser(url).pages
            for info in info_list:
                message = Message(info.to_json())
                channel.basic_publish(message, 'cra-action2-ex')
            # connection.exchange_declare('cra-action2-ex')
        # connection.basic_publish()
else:
    raise Exception(f"File {__name__} cant be imnport")

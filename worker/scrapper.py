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


import logging
from configparser import ConfigParser
from amqp.connection import Connection
from amqp.basic_message import Message
from amqp.channel import Channel
from amqp.spec import Basic
from time import sleep

from core import Info


config = ConfigParser()
config.read('./consumer.ini')

connection_setting = config['CONNECTION']
timeout = int(config['DEFAULT']['timeout'])


with Connection(**connection_setting) as connection:
    channel = connection.channel()

    def on_message(message: Message):
        global channel
        # channel: Channel = message.channel
        info = Info.from_json(message.body)
        print(message.delivery_tag)
        channel.basic_ack(message.delivery_tag)
        # channel.

    channel.basic_consume('cra-action2', callback=on_message)
    channel.confirm_select()


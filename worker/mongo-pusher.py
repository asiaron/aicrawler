"""
mongo-pusher.py

TODO описание модуля

created by alex in aicrawler as 8/6/2020
Проект aicrawler
"""


__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['pavelmstu','alex', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '20200608'

from dataclasses import dataclass, field

from kombu import Queue, Exchange, Connection, Message
from kombu.mixins import ConsumerMixin
from pymongo import MongoClient


@dataclass
class MongoPusher(ConsumerMixin):
    connection: Connection
    in_: Queue = field(default_factory=lambda: Queue('mongo-pusher-in'))
    out: str = 'pages'
    client: MongoClient = field(default_factory=MongoClient)

    def __post_init__(self):
        db = self.client[self.out]
        self.pages_collection = db['pages']

    def get_consumers(self, Consumer, channel):
        return [Consumer(
            queues=[self.in_],
            callbacks=[self.on_task]
        )]

    def on_task(self, body, message: Message):
        self.pages_collection.insert_one(body)
        message.ack()


if __name__ == '__main__':
    with Connection() as connection:
        MongoPusher(connection).run()
else:
    raise Exception(f"File {__name__} can't be import")
"""
monitor.py

TODO описание модуля

created by pavel in pavel as 6/3/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20200603'

# TODO /media/pavel/CryptDisk/AntiIdiot/gitlab/aicrawler/worker/scrapper.py

import argparse
from kombu import Exchange, Connection, Producer

parser = argparse.ArgumentParser(
    description='',  # TODO
)

parser.add_argument(
    '--out',
    dest='output_queue',
    help='Output RabbitMQ queue',
    default='monitor-out-ex'
)

# TODO
# See /media/pavel/CryptDisk/AntiIdiot/gitlab/aicrawler/core/auto/tasks_environment.py
example_task = {
    "task": "parse_rss",
    "kwargs": {
        "url": "http://tass.ru/rss/v2.xml",
        "limit": 10,
        "time_bound": "2020-06-04T10:00"
    }
}

def main(out):
    with Connection() as connection:
        with connection.channel() as channel:
            producer = Producer(channel)
            producer.publish(example_task,exchange=out)

if __name__ == '__main__':
    args = parser.parse_args()
    out = Exchange(args.output_queue)
    main(out)
else:
    raise Exception(f"File {__name__} can't be import")

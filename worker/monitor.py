"""
monitor.py

TODO описание модуля

created by pavel in pavel as 6/3/20
Проект aicrawler
"""

from time import sleep
import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = 'LGPL v3'
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
example_task_message = {
    "task": "parse_rss",
    "kwargs": {
        "url": "http://tass.ru/rss/v2.xml",
        "limit": 100,
        "time_bound": "2020-06-04T10:00"
    }
}


TASKS = [
    {
        "last": datetime.datetime(2000, 1, 1),
        "timedelta": datetime.timedelta(minutes=10),
        "message": example_task_message,
    }
]


def main(out):

    while True:
        for task in TASKS:
            if task['last'] + task['timedelta'] < datetime.datetime.now():
                with Connection() as connection:
                    with connection.channel() as channel:
                        producer = Producer(channel)
                        producer.publish(example_task_message, exchange=out)

                task['last'] = datetime.datetime.now()
            continue
        sleep(10)


if __name__ == '__main__':
    # args = parser.parse_args()
    out = Exchange('monitor-out-ex')#args.output_queue)
    main(out)
else:
    raise Exception(f"File {__name__} can't be import")

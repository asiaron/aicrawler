"""
first_filter.py


~$ python3 -m worker.first_filter

created by pavel in pavel as 5/29/20
Проект aicrawler
"""

import datetime

__author__ = 'pavel'
__maintainer__ = 'pavel'
__credits__ = ['pavel', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20200529'


# TODO argparse

from processing.filters import LabelFilter


fltr = LabelFilter(
    [
        'коронавирус',
        'самоизоляция',
        'экономика',
        'нефть',
        'общество'
    ]
)


def main(args):
    with RabbitConsumer('cra-action1') as cunsumer:
        with RabbitReceiver('cra-action2-ex') as receiver:
            for message in consumer.get_all(infinite=True):
                if fltr(message):
                    receiver.send(message)


if __name__ == "__main__":

    # TODO
    args = {...:...}

    main(args)
else:
    raise Exception('Only run! not import ')

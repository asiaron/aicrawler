"""
first_filter.py

TODO описание модуля

created by pavel in pavel as 6/2/20
Проект aicrawler
"""


__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '20200602'


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

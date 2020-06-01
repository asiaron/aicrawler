"""
__init__.py

TODO описание модуля

created by pavel in pavel as 5/29/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v3"
__status__ = 'Development'
__version__ = '20200529'

from typing import List, Callable

from core import Info
from core.filters import Filter


class LabelFilter(Filter):

    def __init__(self, labels: List[str]):
        labels = [label.lower() for label in labels]

        def _func_rule(message: Info) -> bool:
            nonlocal labels
            # assert 'title' in message
            # assert 'description' in message
            # assert 'preview' in message
            # assert 'subjects' in message
            # assert isinstance(message['subjects'], list)
            # assert isinstance(message['description'], str)
            # assert isinstance(message['preview'], str)
            # assert isinstance(message['title'], str)

            return any(label in message.lower()
                       for message in (message.title, message.description, message.preview, *message.subjects)
                       for label in labels
                       )

        label_repr = ', '.join(labels) if len(labels) < 3 else ', '.join(labels[:2]) + '...'
        super().__init__(func_rule=_func_rule, _list=[label_repr])

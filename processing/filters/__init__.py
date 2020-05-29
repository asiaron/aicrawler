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


from typing import List, Callable, Dict

from core.filters import Filter


class LabelFilter(Filter):

    def __init__(self, labels: List[str]):

        labels = [label.lower() for label in labels]

        def _func_rule(message: Dict) -> bool:
            nonlocal labels
            assert 'title' in message
            assert 'description' in message
            assert 'preview' in message
            assert 'subjects' in message
            assert isinstance(message['subjects'], list)
            assert isinstance(message['description'], str)
            assert isinstance(message['preview'], str)
            assert isinstance(message['title'], str)

            if any(label in message['title'].lower() for label in labels):
                return True
            if any(label in message['description'].lower() for label in labels):
                return True
            if any(label in message['preview'].lower() for label in labels):
                return True
            for subject in message['subjects']:
                if any(label in subject.lower() for label in labels):
                    return True
            return False

        super().__init__(func_rule=_func_rule)

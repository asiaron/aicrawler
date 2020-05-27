"""
__init__.py

TODO описание модуля

created by pavel in pavel as 5/26/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v.3"
__status__ = 'Development'
__version__ = '20200526'

from typing import List, Tuple, Dict, Optional, Callable, Union


from core import BaseCrawler, Page


class RbcCrawler(BaseCrawler):
    """

    """

    MAIN_URL = "https://www.rbc.ru"

    def __init__(self):
        super().__init__()

    def search(self, query: str, limit: int) -> List[Page]:

        raise NotImplementedError("!")


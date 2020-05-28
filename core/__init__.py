"""
__init__.py

TODO описание модуля

created by pavel in pavel as 5/26/20
Проект aicrawler
"""

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v.3"
__status__ = 'Development'
__version__ = '20200526'

from typing import List, Tuple, Dict, Optional, Callable, Union
from collections import namedtuple, UserDict
from dataclasses import dataclass, field
from datetime import datetime

Preview = namedtuple("header", 'text')


class Attachment(object):
    """
    Некое приложение. Например изображение
    """


@dataclass
class Page(object):
    """
    Страница.
    """
    url: str
    _html: str = field(init=False, default=None)

    @property
    def html(self):
        if not self._html:
            self._html = self._collect_html()
        return self._html

    def _collect_html(self) -> str:
        return ""


@dataclass
class NewsPage(Page):
    title: str
    time: datetime = None
    preview: Preview = None
    subjects: List[str] = None


class PageBuilder(UserDict):
    def build_as(self, cls):
        return cls(**self.data)


@dataclass
class Info:
    # Заголовок новости
    header: str

    # Превью новости
    preview: str  # or Null

    # Список url из которых была получена данная новость
    # urls: List[str]

    # основной текст новости
    text: str

    # Время самой новости. Если извлечено из нескольких -- наименьшее
    time: Union[datetime, None]

    attachments: List[Attachment]

    def __add__(self, other):
        assert isinstance(other, Info)
        # TODO проверить, что тексты новостей примерно одинаковые.


class BaseCrawler(object):

    MAIN_URL = None

    def __init__(self):

        assert self.__class__.MAIN_URL, f"Вы не задали MAIN_URL для класса {self.__class__.__name__}"

    def search(self, query: str, limit: int) -> List[Page]:
        """
        Поиск по строке query
        :param query: строка запроса в utf8
        :param limit: максимальное количество выдаваемых данных
        :return:
        """
        return NotImplemented

    @classmethod
    def extract_useful_info(cls, Page):
        return NotImplemented
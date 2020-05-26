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

from collections import namedtuple

from dataclasses import dataclass

Preview = namedtuple("header", 'text')


class Attachment(object):
    """
    Некое приложение. Например изображение
    """


class Page(object):
    """
    Страница.
    """

    def __init__(self, url):
        self._url = url

        self._html = None


    @property
    def url(self):
        return self._url

    @property
    def html(self):
        if self._html:
            return self._html
        raise NotImplementedError("!")


class NewsPage(Page):

    def __init__(self, url, preview: Preview, time: datetime.datetime, subjects: List[str]):
        super().__init__(url)
        self._time = time
        self._preview = preview
        self._subjects = subjects

    @property
    def preview(self):
        return self._preview


@dataclass
class Info():

    # Заголовок новости
    header: str

    # Превью новости
    preview: str  # or Null

    # Список url из которых была получена данная новость
    # urls: List[str]

    # основной текст новости
    text: str

    # Время самой новости. Если извлечено из нескольких -- наименьшее
    time: datetime.datetime  # or Null

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
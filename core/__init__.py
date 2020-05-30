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
from dataclasses import dataclass, field, asdict
from datetime import datetime
from json import dumps, loads

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
    _html: str = field(init=False, default=None, repr=False)

    @property
    def html(self):
        if not self._html:
            self._html = self._collect_html()
        return self._html

    def _collect_html(self) -> str:
        return ""

@dataclass
class TimeZone:
    offset: int
    name: str

@dataclass
class Info:
    """
    description of the docs/json.md
    """
    action: int
    type: str
    source: str
    source_url: str
    title: str
    guid: str
    link: str
    description: str
    preview: str
    subjects: List[str]
    time: datetime
    zone: TimeZone

    def to_json(self) -> str:
        dict_ = asdict(self)
        time: datetime = dict_['datetime']
        dict_['datetime'] = time.isoformat()
        return dumps(dict_)

    @classmethod
    def from_json(cls, json: str):
        dict_ = loads(json)
        iso_time: str = dict_['datetime']
        dict_['datetime'] = datetime.fromisoformat(iso_time)
        zone: Dict = dict_['zone']
        dict_['zone'] = TimeZone(zone)
        return cls(dict_)
    #
    # "action": 1,
    # "type": "rss",
    # "source": "tass",
    # "source_url": "tass.ru",
    # "title": "Комитет Думы поддержал законопроект о праве сотрудников ФСИН объявлять предостережение",
    # "guid": "tass::8574085",
    # "link": "https://tass.ru/obschestvo/8574085",
    # "description": "Инициатива призвана устранить правовую коллизию, когда органы уголовно-исполнительной системы являются субъектами профилактики правонарушений, но необходимых полномочий не имеют",
    # "preview": "Инициатива призвана устранить правовую коллизию, когда органы уголовно-исполнительной системы являются субъектами профилактики правонарушений, но необходимых полномочий не имеют",
    # "subjects": [
    #     "общество"
    # ],
    # "time": "2020.05.27 08:01",
    # "zone": {
    #     "offset": 3,
    #     "name": "MSK"
    # }


class PageBuilder(UserDict):
    def build_as(self, cls):
        return cls(**self.data)


@dataclass
class Info_:
    # Заголовок новости
    header: str

    # Превью новости
    preview: str  # or Null

    # Список link из которых была получена данная новость
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
"""
rss.py

TODO описание модуля

created by pavel in pavel as 5/26/20
Проект aicrawler
"""

import datetime
# import

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v3"
__status__ = 'Development'
__version__ = '20200526'

import requests
from xml.dom.minidom import parseString

from core.auto import BaseAuto, Page


class RssAuto(BaseAuto):
    """
    Просто GET и POST запросы
    """
    @property
    def xml(self):
        if not self._xml:
            self._xml = requests.get(self._url).text
        return self._xml

    @property
    def dom(self):
        if not self._dom:
            self._dom = parseString(self.xml)
        return self._dom

    @classmethod
    def parse_item(cls, item) -> Page:
        title = item.getElementsByTagName("title")[0].firstChild.data
        link = item.getElementsByTagName("link")[0].firstChild.data
        # preview = item.getElementsByTagName("description")[0].firstChild.data
        # subjects = [c.firstChild.data for c in item.getElementsByTagName("category")]
        time = item.getElementsByTagName("pubDate")[0].firstChild.data
        return Page(link)

    def get_pages(self):# -> List[Page]:
        items = self.dom.getElementsByTagName("item")
        pages = [self.parse_item(item) for item in items]

        return pages

    def __init__(self, url):
        self._url = url
        self._xml = None
        self._dom = None

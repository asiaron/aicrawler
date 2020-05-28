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
# noinspection PyUnresolvedReferences
from xml.dom.minidom import parseString
from core.auto import BaseAuto
from core import Page, NewsPage
from typing import List
from feedparser import FeedParserDict
import feedparser

from time import struct_time, mktime
from datetime import datetime
from urllib.parse import urlparse


class RssParser:
    def __init__(self, url):
        self._url = url
        self._netloc = None
        self._pages = None
        self._feed = feedparser.parse(url)

    @property
    def pages(self):
        if not self._pages:
            self._pages = [self.entry_to_page(entry) for entry in self._feed.entries]
        return self._pages

    @property
    def netloc(self):
        if not self._netloc:
            self._netloc = urlparse(self._feed.link).netloc
            if not self._netloc:  # link is invalid
                raise ValueError('link of rss feed is invalid')
        return self._netloc

    def guid_to_page_id(self, guid: str) -> str:
        parsed = urlparse(guid)
        if not parsed.scheme or not parsed.netloc:
            return f'{self.netloc}::{guid}'
        else:
            return f'{parsed.netloc}::{parsed.path[1:]}'  # without leading /, example: '/moskva/1' -> 'moskva/1'

    @staticmethod
    def struct_time_to_datetime(struct: struct_time) -> datetime:
        return datetime.fromtimestamp(mktime(struct))

    def entry_to_page(self, entry: FeedParserDict) -> NewsPage:
        return NewsPage(
            url=entry.link,
            title=entry.title,
            time=self.struct_time_to_datetime(entry.published_parsed),
            # guid=self.guid_to_page_id(entry.guid),
            # timezone=
            preview=entry.get('summary', None),
            subjects=[tag.term for tag in entry.get('tags')]
        )
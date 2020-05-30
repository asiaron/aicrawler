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
from core import Page, Info, TimeZone
from typing import List
from feedparser import FeedParserDict
import feedparser

from time import struct_time, mktime
from datetime import datetime
from urllib.parse import urlparse


class RssParser:
    def __init__(self, url):
        self._link = url
        self._netloc = None
        self._pages = None
        self._site_name = None
        self._rss = feedparser.parse(url)

    @property
    def pages(self):
        if not self._pages:
            self._pages = [self.entry_to_page(entry) for entry in self._rss.entries]
        return self._pages

    @property
    def netloc(self):
        if not self._netloc:
            self._netloc = urlparse(self._rss.feed.link).netloc
            if not self._netloc:  # link is invalid
                raise ValueError('link of rss feed is invalid')
        return self._netloc

    @property
    def site_name(self):
        if not self._site_name:
            self._site_name = '.'.join(self.netloc.split('.')[:-1])
        return self._site_name

    def get_guid(self, guid: str) -> str:
        parsed = urlparse(guid)
        if not parsed.scheme or not parsed.netloc:  # guid used by newspaper is not an url, we use it per se
            return f'{self.site_name}::{guid}'
        else:
            our_guid = parsed.path.split('/')[-1] # take last element as guid: '/moskva/2312' -> '2312'
            return f'{self.site_name}::{our_guid}'

    @staticmethod
    def struct_time_to_datetime(struct: struct_time) -> datetime:
        return datetime.fromtimestamp(mktime(struct))

    def entry_to_page(self, entry: FeedParserDict) -> Info:
        time = entry.published_parsed
        return Info(
            action=1,
            type='rss',
            source='tass',
            source_url=self.netloc,
            title=entry.title,
            guid=self.get_guid(entry.guid),
            link=entry.link,
            description=entry.get('summary', ''),
            preview=entry.get('summary', ''),
            subjects=[tag.term for tag in entry.get('tags')],
            time=self.struct_time_to_datetime(time),
            zone=TimeZone(
                offset=3, #  time.tm_gmtoff /1800,
                name='MSK'  # time.tm_zone
            )
        )

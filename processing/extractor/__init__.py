"""
worker.py

TODO описание модуля

created by alex in alex as 7/5/20
Проект aicrawler
"""


__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['pavelmstu', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '20200605'

from itertools import chain
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag

_registered_extractors = {}


def extractor(netloc: str):
    def register_extractor(callable):
        _registered_extractors[netloc] = callable
        return callable
    return register_extractor


@extractor('tass.ru')
def extract_from_tass(page: str) -> Dict:
    html = BeautifulSoup(page, 'html.parser')
    news = html.find(class_='news')
    header = news.find(class_='news-header__title').text.rstrip('\n')
    description = news.find(class_='news-header__lead').text.rstrip('\n')
    blocks = chain.from_iterable(news.find_all(class_='text-block'))
    text_blocks = (' '.join(el for el in block.text.strip().split() if el)  # clear block whitespacing
                   for block in blocks if block.name in ('p', 'h2'))
    message = {
        'body': '\n'.join(block for block in text_blocks)
    }
    return message


@extractor('ria.ru')
def extract_from_ria(page):
    html = BeautifulSoup(page, 'html.parser')
    article = html.find(class_='article')
    header = html.find(class_='article__title').text.rstrip('\n')
    blocks = list(chain.from_iterable(article.find_all(class_='article__block', attrs={'data-type': 'text'})))
    text_blocks = (' '.join(el for el in block.text.strip().split() if el)  # clear block whitespacing
                   for block in blocks)
    message = {
        'body': '\n'.join(block for block in text_blocks)
    }
    return message


def default_extractor(page: str) -> Dict:
    raise ValueError('Only tass resources supports')


def extract_text(page: str, netloc: str, rss: Dict = None) -> Dict:
    rss = rss if rss is None else {}
    extractor = _registered_extractors.get(netloc, default_extractor)
    return extractor(page)



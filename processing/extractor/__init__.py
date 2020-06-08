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


def extract_from_tass(page: str) -> Dict:
    html = BeautifulSoup(page, 'html.parser')
    news = html.find(class_='news')
    header = news.find(class_='news-header__title').text.rstrip('\n')
    description = news.find(class_='news-header__lead').text.rstrip('\n')
    blocks = chain.from_iterable(news.find_all(class_='text-block'))
    text_blocks = (block.text for block in blocks if block.name in ('p', 'h2'))
    message = {
        'body' : '\n'.join(block for block in text_blocks)
    }
    return message


def extract_text(page: str, source: str) -> Dict:
    if source == 'tass.ru':
        return extract_from_tass(page)
    else:
        raise ValueError('Only tass resources supports')


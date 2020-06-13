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
from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import Tag

_registered_extractors = {}


def extractor(netloc: str):
    def register_extractor(callable):
        _registered_extractors[netloc] = callable
        return callable
    return register_extractor


@dataclass
class ArticleTextExtractor:
    article: Dict
    text_blocks: Dict
    # description: Dict = None
    # title: Dict = None

    def __call__(self, page):
        html = BeautifulSoup(page, 'html.parser')
        article = html.find(**self.article)
        blocks = chain.from_iterable(article.find_all(**self.text_blocks))
        text_blocks = (' '.join(el for el in block.text.strip().split() if el)  # clear block whitespacing
                       for block in blocks if hasattr(block, 'text'))
        return {
            'body': '\n'.join(block for block in text_blocks)
        }


extractor('tass.ru')(ArticleTextExtractor({'class_': 'news'}, {'class_': 'text-block'}))
extractor('ria.ru')(ArticleTextExtractor({'class_': 'article'}, {'class_': 'article__block', 'attrs': {'data-type': 'text'}}))
extractor('regnum.ru')(ArticleTextExtractor({'class_': 'article-container'}, {'class_': 'article-text', 'limit': -1}))
extractor('www.interfax.ru')(ArticleTextExtractor({},{}))


def default_extractor(page: str) -> Dict:
    html = BeautifulSoup(page, 'html.parser')
    article = html.find('article')
    if article:
        raw = article.text
        text = '\n'.join(' '.join(word.strip() for word in block.split(' ') if word) for block in raw.split('\n') if block)
        return {
            'body': text
        }
    else:
        raise NotImplementedError(f'Can\'t parse page with default extractor')


def extract_text(page: str, netloc: str, rss: Dict = None) -> Dict:
    rss = rss if rss is None else {}
    extractor = _registered_extractors.get(netloc, default_extractor)
    return extractor(page)

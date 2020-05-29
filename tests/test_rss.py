import responses
from datetime import datetime, timezone, timedelta
import json

import pytest

from core.auto.rss import RssParser
from core import NewsPage


@pytest.fixture('session')
def tass_pages():
    rss = RssParser(open("example_rss.xml").read())
    return rss.pages


@pytest.fixture('session')
def example_page(tass_pages):
    return tass_pages[0]


@pytest.fixture('session')
def example_page_json():
    return json.dumps(json.load(open('example_page.json')))  # to cope with whitespaces


@pytest.fixture('session')
def ideal_tass_third_page():
    return NewsPage(url='https://tass.ru/moskovskaya-oblast/8573937',
                    title='Передвижные пункты вакцинации животных против бешенства заработали в Подмосковье',
                    # guid='tass.ru::moskva/8591843',
                    time=datetime(2020, 5, 27, 8, 00, 45, 0),  # , timezone(timedelta(hours=3))),
                    preview='В регионе работает 55 выездных бригад ветеринарных специалистов',
                    subjects=['Московская область']
                    )


def test_parsed_page_format(tass_pages, ideal_tass_third_page):
    assert tass_pages[2] == ideal_tass_third_page


def test_number_of_parsed_pages(tass_pages):
    assert len(tass_pages) == 99


@pytest.mark.skip('to_json yet is not implemented')
def test_json_representation_of_page(example_page):
    assert example_page.to_json() == example_page


if __name__ == '__main__':
    pytest.main()

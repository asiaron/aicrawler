import responses
from datetime import datetime, timezone, timedelta

import pytest

from core.auto.rss import RssParser
from core import NewsPage


def test_rss():
    rss = RssParser(open("example_rss.xml").read())
    pages = rss.pages
    assert pages[8].url == "https://tass.ru/ekonomika/8573963"
    assert pages[2] == NewsPage(url='https://tass.ru/moskovskaya-oblast/8573937',
                                title='Передвижные пункты вакцинации животных против бешенства заработали в Подмосковье',
                                # guid='tass.ru::moskva/8591843',
                                time=datetime(2020, 5, 27, 8, 00, 45, 0), #, timezone(timedelta(hours=3))),
                                preview='В регионе работает 55 выездных бригад ветеринарных специалистов',
                                subjects=['Московская область']
                                )


if __name__ == '__main__':
    pytest.main()

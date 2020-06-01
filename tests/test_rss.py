import responses
from datetime import datetime, timezone, timedelta
import json

import pytest

from core.auto.rss import RssParser
from core import Info, TimeZone


@pytest.fixture(scope='session')
def tass_info():
    rss = RssParser(open("example_rss.xml").read())
    return rss.pages


@pytest.fixture(scope='session')
def example_info_json():
    return json.dumps(json.load(open('example_page.json')))  # cope with whitespaces


@pytest.fixture(scope='session')
def ideal_tass_third_info():
    return Info(
        action=1,
        type='rss',
        source='tass',
        source_url='tass.ru',
        title='Передвижные пункты вакцинации животных против бешенства заработали в Подмосковье',
        guid='tass::8573937',
        link='https://tass.ru/moskovskaya-oblast/8573937',
        description='В регионе работает 55 выездных бригад ветеринарных специалистов',
        preview='В регионе работает 55 выездных бригад ветеринарных специалистов',
        time=datetime(2020, 5, 27, 8, 0, 45, 0),  # '2020-05-27T08:00:45',
        subjects=[
            'московская область'
        ],
        zone=TimeZone(
            offset=3,
            name='MSK'
        )
    )


def test_parsed_page_format(tass_info, ideal_tass_third_info):
    assert tass_info[2] == ideal_tass_third_info


def test_number_of_parsed_pages(tass_info):
    assert len(tass_info) == 99


# @pytest.mark.skip('to_json yet is not implemented')
def test_json_representation_of_info(ideal_tass_third_info, example_info_json):
    assert ideal_tass_third_info.to_json() == example_info_json


# @pytest.mark.skip('from_json yet is not implemented')
def test_restoration_info_from_json(ideal_tass_third_info, example_info_json):
    assert ideal_tass_third_info == Info.from_json(example_info_json)


if __name__ == '__main__':
    pytest.main(['test_rss.py'])

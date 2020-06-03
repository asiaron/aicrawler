from datetime import datetime, timezone, timedelta
import json
from copy import deepcopy

import pytest

from core import Info, TimeZone
from core.auto.rss import RssParser
# from core.filters import Filter
from processing.filters import LabelFilter


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
        time=datetime(2020, 5, 27, 8, 0, 45, 0),
        subjects=[
            'московская область'
        ],
        zone=TimeZone(
            offset=3,
            name='MSK'
        )
    )


# Filters


@pytest.fixture(scope='session')
def covid_filter():
    covid_words = ['коронавирус', 'COVID', 'карантин']
    return LabelFilter(labels=covid_words)


@pytest.fixture(scope='session')
def not_covid_disease_filter():
    disease_words = ['АЧС', 'бешенств']
    return LabelFilter(labels=disease_words)


@pytest.fixture(scope='session')
def economic_filter():
    economic_words = ['экономик', 'бизнес']
    return LabelFilter(labels=economic_words)

# Info for testing filters


@pytest.fixture(scope='session')
def economic_info(tass_info):
    return tass_info[52]


@pytest.fixture(scope='session')
def vaccination_rabies_info(tass_info):
    return tass_info[2]


@pytest.fixture(scope='session')  # карантин
def achs_virus_info(tass_info):
    return tass_info[38]


@pytest.fixture(scope='session')
def covid_info_in_subjects_only(tass_info):
    return tass_info[90]


@pytest.fixture(scope='session')
def covid_info_in_title_only(tass_info):
    info = deepcopy(tass_info[93])
    del info.subjects[1]  # covid related
    return info

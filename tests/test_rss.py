import responses
from datetime import datetime, timezone, timedelta
import json

import pytest

from core.auto.rss import RssParser, netloc_to_source
from core import Info, TimeZone

from tests.mock_objects import tass_info, ideal_tass_third_info, example_info_json


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


@pytest.mark.parametrize('netloc,source', [
    ('rss.ru', 'rss'), ('ria.ru', 'ria'), ('www.interfax.ru', 'interfax'),
    # ('russian.rt.com', 'rt')
])
def test_netloc_to_source(netloc: str, source: str):
    assert netloc_to_source(netloc) == source


if __name__ == '__main__':
    pytest.main(['test_rss.py'])

"""
test_extractor.py

TODO описание модуля

created by alex in aicrawler as 9/6/2020
Проект aicrawler
"""


__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['pavelmstu','alex', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '200609'

import pytest

from json import load

from processing.extractor import extract_text

PATH_TO_MOCK = 'tests/mock_objects/'

# source prefix for mock files
extract_text_data = [
    ('tass', 'tass.ru'),
    ('ria', 'ria.ru')
]


@pytest.mark.parametrize('source,netloc', extract_text_data)
def test_extract_text(source, netloc):
    page = open(PATH_TO_MOCK + source + '_page.html').read()
    extracted_ideal = load(open(PATH_TO_MOCK + source + '_extract_entry.json'))
    extracted = extract_text(page, netloc)
    assert extracted == extracted_ideal

"""
test_extractor.py

TODO описание модуля

created by alex in alex as 7/5/20
Проект aicrawler
"""


__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = 'LGPL v3'
__status__ = 'Development'
__version__ = '20200605'

import requests
from typing import Dict, List

from core import Info
from core.auto.worker import Worker
from processing.extractor import extract_text


class Extractor(Worker):
    def process_message(self, message: str) -> List[Dict]:
        info = Info.from_json(message)
        page = requests.get(info.link)
        text = extract_text(page.text, info.source_url)
        if text:
            return [{
                '_id': info.link,
                'source': info.source_url,
                'title': info.title,
                'body': text['body']
            }]
        else:
            return []


if __name__ == '__main__':
    Extractor.run_from_args('extractor')
else:
    raise Exception(f"File {__name__} can't be import")

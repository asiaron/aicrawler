"""

# TODO

"""

__author__ = 'alex'
__maintainer__ = 'alex'
__credits__ = ['alex', 'pavelmstu']
__copyright__ = 'LGPL v.3'
__status__ = 'Development'
__version__ = '20200602'

import json

from core.auto.worker import Worker
from typing import Iterable


# ! не убирать
import processing.scrapper.imports

from core.auto.tasks_environment import get_scrapper_func


class Scrapper(Worker):
    def process_message(self, body: str) -> Iterable[str]:
        message = json.loads(body)
        task = message['task']
        kwargs = message['kwargs']

        func = get_scrapper_func(task)
        if func is None:
            # ... TODO
            raise Exception(f"Нет {task} функции!")

        return (page.to_json() for page in func(**kwargs))


if __name__ == '__main__':
    Scrapper.run_from_args('scrapper')
else:
    raise Exception(f"File {__name__} can't be import")

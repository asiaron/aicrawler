"""
tasks_envioroment.py

TODO описание модуля

created by pavel in pavel as 6/3/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v3"
__status__ = 'Development'
__version__ = '20200603'


from functools import wraps

# from core.auto.rss import RssParser


# TODO лучше сделать функцию ! RssParser

_TASKS_ENVIRONMENT = {
    # "class.RssParser": RssParser,
}
# RssParser(**kwargs)/media/pavel/CryptDisk/AntiIdiot/gitlab/aicrawler/core/auto/tasks_environment.py


def scrapper_task(func):

    @wraps(func)
    def inner(**kwargs):

        ret_ = func(**kwargs)

        return ret_

    assert inner.__name__ not in _TASKS_ENVIRONMENT.keys(), f"Функция {inner.__name__} уже существует. Смените имя"

    _TASKS_ENVIRONMENT[inner.__name__] = inner

    return inner

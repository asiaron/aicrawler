"""
auto.py

TODO описание модуля

created by pavel in pavel as 5/26/20
Проект aicrawler
"""


from typing import Union

from core import Page


class BaseAuto(object):
    """
    Базовый бот для краулинга
    """
    pass

    # Время сна после open операции
    AFTER_OPEN_TIMEOUT = 1

    def open(self, url: Union[str, Page]):
        """
        Первоначальный заход браузера на страницу
        :param url:
        :return:
        """
        return NotImplemented

    def goto(self, page: Page) -> bool:
        """
        Поиск текущего Page и переход
        :param page:
        :return:
        True -- элемент найден и браузер перешёл на него
        False -- элемент не найден и браузер не перешёл на него
        """
        return NotImplemented

    def get_page(self) -> Page:
        """
        Возвращает текущую страницу
        :return:
        """
        return NotImplemented

    # def __enter__(self):
    # ....

    # def __exit__(self, exc_type, exc_val, exc_tb):
    # ....


"""
__init__.py

TODO описание модуля

created by pavel in pavel as 5/26/20
Проект aicrawler
"""

import datetime

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "LGPL v.3"
__status__ = 'Development'
__version__ = '20200526'

from typing import List, Tuple, Dict, Optional, Callable, Union, Any
from math import ceil
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from datetime import datetime

from core import BaseCrawler, Page


class RbcCrawler(BaseCrawler):
    """

    """

    MAIN_URL = "https://www.rbc.ru"
    QUERY_TEMPLATE = "https://www.rbc.ru/search/?project=rbcnews&query={query}"

    def __init__(self, webdriver: WebDriver):
        super().__init__()
        self._webdriver = webdriver

    @staticmethod
    def count_urls_to_pages(n_urls: int) -> int:
        return ceil(n_urls/10 - 1)

    def scroll_down(self) -> None:
        self._webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(2)  # maybe implement intelective waiting by counting of objects? or stretching down the body

    def do_query(self, query: str) -> None:
        url = self.QUERY_TEMPLATE.format(query=query)
        # print(self._webdriver, link)
        self._webdriver.get(url)

    def form_datetime(date: str, time: str) -> datetime:
        pass
        # TODO
        # 11 сен 2019
        # 

    @classmethod
    def get_data_from_element(cls, element: WebElement) -> Dict[str, Any]:
        data = {}
        data["link"] = element.find_element_by_class_name("search-item__link").get_attribute("href")
        data["title"] = element.find_element_by_class_name("search-item__title").text
        data["preview"] = element.find_element_by_class_name("search-item__text").text

        more = element.find_element_by_class_name("search-item__category").text
        more_list = more.split(", ")

        # # category, date, time format
        
        # if len(more) == 3: # category, date, time format
        #     data["category"], date, time = more_list
        # else if len(more) == 2: # date, time format
        #     date, time = more_list
        # else:

        # data["datetime"] = cls

        return data 

    @staticmethod
    def form_page(data: Dict[str, Any]) -> Page:
        return Page(data["link"])
        
    def collect_elements(self, limit: int) -> List[WebElement]:
        return self._webdriver.find_elements_by_class_name("search-item")[:limit]

    def search(self, query: str, limit: int) -> List[Page]:
        self.do_query(query)

        for time_of_scroll in range(self.count_urls_to_pages(limit) - 1):
            self.scroll_down()
        
        elements = self.collect_elements(limit)
        data = (self.get_data_from_element(element) for element in elements)
        pages = [self.form_page(datum) for datum in data]
        
        return list(pages)


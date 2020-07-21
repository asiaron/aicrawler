#  """
#  __init__.py
#
#  TODO описание модуля
#
#  created by alex in aicrawler as 15/6/2020
#  Проект aicrawler
#  """
#
#
#  __author__ = 'alex'
#  __maintainer__ = 'alex'
#  __credits__ = ['pavelmstu','alex', ]
#  __copyright__ = 'LGPL v3'
#  __status__ = 'Development'
#  __version__ = '200615'

from typing import List

from urllib.parse import urlencode, urlunsplit

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def form_url(query: str, page: int) -> str:
    encoded = urlencode({
        #'page': [page],
        'query': [query],
        #'submit': ['Submit']
    }, doseq=True)
    return urlunsplit(['https', 'www.springer.com', '/gp/search', encoded, ''])


def get_resource_urls(browser: Chrome) -> List[str]:
    entries = browser.find_elements(By.CLASS_NAME, 'result-item')
    links = [
        entry.find_element(By.TAG_NAME, 'a').get_attribute('href')
        for entry in entries
        if entry.find_element(By.CLASS_NAME, 'result-type').text != 'Web Pages'
    ]
    return links


def search_resources(browser: Chrome, query: str, limit: int = 10) -> List[str]:
    url = form_url(query, 0)
    browser.get(url)

    results_form = browser.find_element(By.CLASS_NAME, 'result-count-message')
    n_results = results_form.text.split(' ')[1]
    print(n_results)

    urls = get_resource_urls(browser)
    valid_urls = [url for url in urls if
    return urls

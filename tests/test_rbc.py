from selenium.webdriver import Chrome
import pytest

from processing import *


@pytest.fixture(scope="module")
def webdriver():
    wd = Chrome()
    yield wd
    wd.close()


@pytest.mark.skip('skip')
def test_getting_urls_from_rbc_crawler(webdriver):
    # webdriver = Chrome()
    crawler = RbcCrawler(webdriver)
    # link = crawler.QUERY_TEMPLATE.format(query="бизнес")
    # crawler._webdriver.get(link)
    # crawler.do_query("buisness")
    pages = crawler.search("бизнес", 35)
    assert len(pages) == 35

# def test_my(webdriver):
    # print(webdriver)
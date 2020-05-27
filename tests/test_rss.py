import responses
from core.auto.rss import RssAuto


@responses.activate
def test_rss_crawler():
    responses.add(responses.GET, "http://tass.ru/rss/v2.xml",
                  body=open("example_rss.xml").read())
    rss = RssAuto("http://tass.ru/rss/v2.xml")
    pages = rss.get_pages()
    assert pages[8].url == "https://tass.ru/ekonomika/8573963"

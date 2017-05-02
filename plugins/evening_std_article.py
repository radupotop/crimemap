from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

class EveningStdArticle():
    """
    The Evening Standard Article scraper.
    """

    @classmethod
    def scrape(cls, url):
        resp = requests.get(url)
        page = BeautifulSoup(resp.content, 'lxml')
        article = page.article

        _scraped = {
            'title': article.header.h1.text.strip(),
            'author': article.header.find(class_='author').text.strip(),
            'published_datetime': datetime.fromtimestamp(int(int(article.header.time.get('unixtime'))/1000)),
            'scrape_datetime': datetime.utcnow(),
            'media': json.dumps([img.get('src') for img in article.find_all('img') if img.get('title')]),
            'href': url,
            'content': "\n".join([art.text for art in article.find_all('p')])
        }

        return _scraped

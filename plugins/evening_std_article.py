from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

class EveningStdArticle():
    """
    The Evening Standard Article scraper.
    """

    @staticmethod
    def __join_par(element):
        return "\n".join([p.text for p in element.find_all('p')])

    @classmethod
    def scrape(cls, url):
        resp = requests.get(url)
        page = BeautifulSoup(resp.content, 'lxml')
        article = page.article

        _intro = article.header.find(class_='intro')
        _infobox = article.find(class_='ines_infobox')

        _scraped = {
            'title': article.header.h1.text.strip(),
            'subtitle': _intro.text.strip() if _intro else None,
            'author': article.header.find(class_='author').text.strip(),
            'published_datetime': datetime.fromtimestamp(int(int(article.header.time.get('unixtime'))/1000)),
            'scrape_datetime': datetime.utcnow(),
            'media': json.dumps([img.get('src') for img in article.find_all('img') if img.get('title')]),
            'meta': json.dumps({'tags':[tag.text for tag in article.find_all(attrs={'itemprop': 'keywords'})]}),
            'href': url,
            'content': cls.__join_par(article),
            'aside': cls.__join_par(_infobox) if _infobox else None,
        }

        return _scraped

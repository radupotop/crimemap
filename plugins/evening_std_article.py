from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .base_scraper import BaseScraper


class EveningStdArticle(BaseScraper):
    """
    The Evening Standard Article scraper.
    """
    type = 'article'

    @staticmethod
    def __join_par(element):
        return "\n".join([p.text for p in element.find_all('p')])

    @classmethod
    def scrape(cls, url):
        resp = requests.get(url)
        page = BeautifulSoup(resp.content, 'lxml')
        article = page.article

        if not article:
            return

        _intro = article.find(class_='intro')
        _published = article.time.get('unixtime') if hasattr(article, 'time') else None
        _author = article.find(class_='author')
        _infobox = article.find(class_='ines_infobox')

        _scraped = {
            'title': article.h1.text.strip() if hasattr(article, 'h1') else None,
            'subtitle': _intro.text.strip() if _intro else None,
            'author': _author.text.strip() if _author else None,
            'published_datetime': datetime.fromtimestamp(int(int(_published)/1000)) if _published else None,
            'scrape_datetime': datetime.utcnow(),
            'media': [img.get('src') for img in article.find_all('img') if img.get('title')],
            'meta': {'tags': [tag.text for tag in article.find_all(attrs={'itemprop': 'keywords'})]},
            'href': url,
            'content': cls.__join_par(article),
            'aside': cls.__join_par(_infobox) if _infobox else None,
        }

        return _scraped

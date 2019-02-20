from bs4 import BeautifulSoup
import requests
import time
import re
from utils import get_hash
from datetime import datetime
from pprint import pprint
from .base_scraper import BaseScraper
from urllib.parse import urlparse


class EveningStd(BaseScraper):
    """
    The Evening Standard basic scraper.
    """
    type = 'index'
    img_regex = re.compile(r'url\([\'\"](.*)[\'\"]\)', re.I)

    @classmethod
    def _get_image_url(cls, img_elem):
        imagesrc = img_elem.get('data-original')
        if imagesrc:
            return imagesrc

        style = img_elem.get('style')
        if style:
            url = cls.img_regex.findall(style)[0]
            return url

    @classmethod
    def _scrape_article(cls, article):
        """
        Scrape an article and return its data
        """
        _title = article.find('h1')
        _img = article.find(class_='image')

        if not (_title and _title.a): return

        _article = {
            'title': _title.text.strip(),
            'href': cls.base_url + _title.a.get('href'),
            'image': cls._get_image_url(_img) if _img else None,
            'scrape_datetime': datetime.utcnow(),
        }

        _article['hash'] = get_hash(_article['title'], _article['href'])

        return _article

    @classmethod
    def scrape(cls, url):
        """
        Scrape entire page.
        """
        resp = requests.get(url)
        page = BeautifulSoup(resp.content, 'lxml')
        articles = page.find_all('article')

        cls.base_url = '://'.join(urlparse(url)[:2])
        return [cls._scrape_article(art) for art in articles if hasattr(art.h1, 'a')]

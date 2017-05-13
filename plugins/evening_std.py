from bs4 import BeautifulSoup
import requests
import time
import json
import re
from datetime import datetime
from pprint import pprint


class EveningStd():
    """
    The Evening Standard basic scraper.
    """
    base_url    = 'http://www.standard.co.uk'
    resource_url = '/news/crime/'

    @classmethod
    def _get_image_url(cls, img_elem):
        imagesrc = img_elem.get('data-original')
        if imagesrc:
            return imagesrc

        style = img_elem.get('style')
        if style:
            url = re.findall(r'url\([\'\"](.*)[\'\"]\)', style, flags=re.IGNORECASE)[0]
            return url

    @classmethod
    def _scrape_article(cls, article):
        """
        Scrape an article and return its data
        """
        _title = article.find('h1')
        _img = article.find(class_='image')

        if not _title: return

        _article = {
            'title': _title.text.strip(),
            'href': cls.base_url + _title.a.get('href'),
            'image': cls._get_image_url(_img) if _img else None,
            'scrape_datetime': datetime.utcnow(),
        }

        return _article

    @classmethod
    def scrape(cls):
        """
        Scrape entire page.
        """
        resp = requests.get(cls.base_url + cls.resource_url)
        page = BeautifulSoup(resp.content, 'lxml')
        articles = page.find_all('article')

        return [cls._scrape_article(art) for art in articles if hasattr(art.h1, 'a')]

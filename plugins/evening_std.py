# Evening Standard basic scraper

from bs4 import BeautifulSoup
import requests
import time
import json
from datetime import datetime
from haslib import sha256
from pprint import pprint

import model

base_url    = 'http://www.standard.co.uk'  
scraped_url = 'http://www.standard.co.uk/news/crime/'

def _scrape_article(article):
    _title = article.find('h1')
    _img = article.find(class_='image')
    
    if not _title: return
    
    _article_data = {
        'title': _title.text.strip(),
        'href': base_url + _title.a.get('href'),
        'image': _img.get('data-original') or _img.get('style') if _img else None
    }

    _article_data['hash'] = sha256(json.dumps(_article_data).encode()).hexdigest()
    _article_data['scrape_datetime'] = datetime.utcnow()

    return _article_data

def scrape():
    resp = requests.get(scraped_url)
    page = BeautifulSoup(resp.content)
    articles = page.find_all('article')

    return [_scrape_article(art) for art in articles if hasattr(art.h1, 'a')]


while True:
    _file = open('crime.json', 'a')
    _result = scrape()
    pprint(_result)
    json.dump(_result, _file, indent=True)
    _file.close()
    time.sleep(3600)

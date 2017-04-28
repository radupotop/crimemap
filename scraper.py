from bs4 import BeautifulSoup
import requests
from pprint import pprint

# Evening Standard basic scraper
base_url    = 'http://www.standard.co.uk'  
scraped_url = 'http://www.standard.co.uk/news/crime/'

def _scrape_article(article):
    _title = article.find('h1')
    _img = article.find(class_='image')
    
    if not _title: return
    
    return {
        'title': _title.text,
        'href': base_url + _title.a.get('href'),
        'image': _img.get('data-original') or _img.get('style') if _img else None
    }

def scrape():
    resp = requests.get(scraped_url)
    page = BeautifulSoup(resp.content)
    articles = page.find_all('article')

    return [_scrape_article(art) for art in articles if hasattr(art.h1, 'a')]


pprint(scrape())

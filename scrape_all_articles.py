#!/usr/bin/env python3

from model import Base, ArticleIndex, ArticleContent
from plugins import EveningStd, EveningStdArticle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Scraper')
log.setLevel(logging.DEBUG)

db = create_engine('postgresql://postgres@localhost/crimemap')
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)

def run_all_article_contents():
    log.info('Scraping')
    session = DBSession()

    all_idx = session.query(ArticleIndex).all()

    for art in all_idx:
        try:
            scraped_article = EveningStdArticle.scrape(art.href)

            if not scraped_article:
                continue

            model = ArticleContent(**scraped_article)
            model.index_hash = art.hash
            pprint(model)
            session.add(model)
            session.commit()

        except IntegrityError:
            # nothing to do, we've already seen this article
            pass

    session.close()


run_all_article_contents()

#!/usr/bin/env python3

from model import Base, ArticleIndex, ArticleContent
from plugins import EveningStd, EveningStdArticle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('AllArticles')
log.setLevel(logging.DEBUG)

db = create_engine('postgresql://postgres@localhost/crimemap')
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)


def run_all_article_contents():
    log.info('Scraping')
    session = DBSession()

    all_idx = session.query(ArticleIndex).all()

    for art in all_idx:
        scraped_article = EveningStdArticle.scrape(art.href)

        if not scraped_article:
            continue

        model = ArticleContent(**scraped_article)
        model.index_hash = art.hash
        session.add(model)

        try:
            session.commit()
            log.info(model)
        except IntegrityError:
            # we've already seen this article
            session.rollback()

    session.close()


run_all_article_contents()

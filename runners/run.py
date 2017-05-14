#!/usr/bin/env python3

from model import Base, ArticleIndex, ArticleContent
from plugins import EveningStd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
from datetime import datetime, timedelta
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Scraper')
log.setLevel(logging.DEBUG)

db = create_engine('postgresql://postgres@localhost/crimemap')
Base.metadata.create_all(db)
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)

class Runners():
    """
    Scrape Runners
    """
    sleep = 3600

    @classmethod
    async def run_index(cls):
        """
        Article index task
        """
        while True:
            log.info('Scraping index...')
            session = DBSession()
            articles = EveningStd.scrape()
            article_models = [ArticleIndex(**art) for art in articles]

            for art_mdl in article_models:
                session.add(art_mdl)
                try:
                    session.commit()
                    log.info(art_mdl)
                except IntegrityError:
                    # entry exists
                    session.rollback()

            session.close()
            pprint('----')
            await asyncio.sleep(cls.sleep)

    @classmethod
    async def run_recent_content(cls):
        """
        Article content task
        """
        while True:
            await asyncio.sleep(10)
            log.info('Scraping recent content...')
            session = DBSession()

            x_time_ago = datetime.utcnow() - timedelta(days=1)
            all_articles_idx = session.query(ArticleIndex).filter(ArticleIndex.scrape_datetime > x_time_ago).all()

            for art in all_articles_idx:
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
            pprint('----')
            await asyncio.sleep(cls.sleep)



loop = asyncio.get_event_loop()
asyncio.ensure_future(Runners.run_index(), loop=loop)
asyncio.ensure_future(Runners.run_recent_content(), loop=loop)

loop.run_forever()
loop.close()

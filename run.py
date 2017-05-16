#!/usr/bin/env python3

from model import Base, ArticleIndex, ArticleContent, Source
import plugins

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
from datetime import datetime, timedelta
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Scrape')
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
    async def run_index(cls, source):
        """
        Article index task
        """
        while True:
            Plugin = getattr(plugins, source.plugin)
            log.info('Scraping Source {} with Plugin {} on {}'.format(source.name, Plugin.__name__, datetime.utcnow().isoformat()))
            articles = Plugin.scrape(source.scrape_href)
            article_models = [ArticleIndex(**art) for art in articles]
            session = DBSession()

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
            log.info('Scraping recent content...   ' + datetime.utcnow().isoformat())
            session = DBSession()

            x_time_ago = datetime.utcnow() - timedelta(days=1)
            all_articles_idx = session.query(ArticleIndex).filter(ArticleIndex.scrape_datetime > x_time_ago).all()

            for art in all_articles_idx:
                Plugin = getattr(plugins, 'EveningStdArticle')
                scraped_article = Plugin.scrape(art.href)

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

    @classmethod
    def get_sources(cls):
        session = DBSession()
        news_sources = session.query(Source).all()
        session.close()
        return news_sources

    @classmethod
    def run(cls):
        """
        Run event loop with tasks.
        """
        loop = asyncio.get_event_loop()

        for source in cls.get_sources():
            asyncio.ensure_future(cls.run_index(source), loop=loop)

        asyncio.ensure_future(cls.run_recent_content(), loop=loop)

        loop.run_forever()
        loop.close()


Runners.run()

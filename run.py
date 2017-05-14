#!/usr/bin/env python3

from model import Base, ArticleIndex, Borough
from plugins import EveningStd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Scraper')
log.setLevel(logging.DEBUG)

db = create_engine('postgresql://postgres@localhost/crimemap')
Base.metadata.create_all(db)
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)

async def run_article_index():
    """
    Article index task
    """
    while True:
        log.info('Scraping')
        session = DBSession()
        articles = EveningStd.scrape()
        article_models = [ArticleIndex(**art) for art in articles]

        for art_mdl in article_models:
            session.add(art_mdl)
            try:
                session.commit()
                log.info('Created entry: {}'.format(art_mdl.hash))
            except IntegrityError:
                # entry exists
                session.rollback()

        session.close()
        pprint('----')
        await asyncio.sleep(3600)


loop = asyncio.get_event_loop()
asyncio.ensure_future(run_article_index(), loop=loop)

loop.run_forever()
loop.close()

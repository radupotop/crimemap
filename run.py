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

db = create_engine('mysql+pymysql://root@localhost/crimemap')
Base.metadata.create_all(db)
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)

async def run_article_index():
    """
    Article index task
    """
    while True:
        session = DBSession()
        articles = EveningStd.scrape()
        log.info('Scraping')

        for art in articles:
            try:
                art_mdl = ArticleIndex(**art)
                session.add(art_mdl)
                session.commit()
                log.info('Created entry: {}'.format(art['hash']))
            except (IntegrityError, InvalidRequestError):
                # entry exists
                pass

        session.close()
        pprint('----')
        await asyncio.sleep(3600)


loop = asyncio.get_event_loop()
asyncio.ensure_future(run_article_index(), loop=loop)

loop.run_forever()
loop.close()

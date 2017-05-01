#!/usr/bin/env python3

from model import Base, ArticleIndex
from plugins import EveningStd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from pprint import pprint
import logging
import time

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Scraper')
log.setLevel(logging.DEBUG)

db = create_engine('mysql+pymysql://root@localhost/crimemap')
Base.metadata.create_all(db)
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)

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
    time.sleep(3600)

#!/usr/bin/env python3

from model import Base, ArticleIndex
from plugins import EveningStd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import logging
import time

log=logging.getLogger('Scraper')
log.setLevel(logging.DEBUG)


db = create_engine('mysql+pymysql://root@localhost/crimemap')
Base.metadata.create_all(db)
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)
session = DBSession()

while True:

    articles = EveningStd.scrape()

    for art in articles:
        try:
            art_mdl = ArticleIndex(**art)
            session.add(art_mdl)
            session.commit()
        except (IntegrityError, InvalidRequestError):
            log.warning('Entry already exists: {}'.format(art['hash']))

    time.sleep(3600)

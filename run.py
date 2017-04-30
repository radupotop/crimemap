#!/usr/bin/env python3

from model import ArticleIndex
from plugins import EveningStd

from sqlalchemy import create_engine


# db = create_engine('mysql://root@localhost/crimemap')


# while True:
#     _file = open('crime.json', 'a')
#     _result = scrape()
#     pprint(_result)
#     json.dump(_result, _file, indent=True)
#     _file.close()
#     time.sleep(3600)

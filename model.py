import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql as pg
from utils import get_hash

Base = declarative_base()

class ArticleIndex(Base):
    __tablename__ = 'article_index'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    hash = sa.Column(sa.String(64), unique=True, nullable=False)
    scrape_datetime = sa.Column(sa.DateTime())
    title = sa.Column(sa.Text())
    href = sa.Column(sa.Text())
    image = sa.Column(sa.Text())

    def __repr__(self):
        return '<ArticleIndex {} with Title {}>'.format(self.hash, self.title)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.hash:
            self.hash = get_hash(self.title, self.href)


class ArticleContent(Base):
    __tablename__ = 'article_content'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    title = sa.Column(sa.String(255))
    subtitle = sa.Column(sa.String(255))
    href = sa.Column(sa.String(255))
    author = sa.Column(sa.String(255))
    content = sa.Column(sa.Text())
    aside = sa.Column(sa.Text())
    media = sa.Column(pg.JSONB()) #images, video in JSON format
    meta = sa.Column(pg.JSONB()) #tags, other stuff in JSON format
    published_datetime = sa.Column(sa.DateTime())
    scrape_datetime = sa.Column(sa.DateTime())
    index_hash = sa.Column(sa.String(64), sa.ForeignKey('article_index.hash'), nullable=False)

    def __repr__(self):
        return '<ArticleContent {} with Title {}>'.format(self.index_hash, self.title)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.index_hash:
            self.index_hash = get_hash(self.title, self.href)

class Borough(Base):
    __tablename__ = 'boroughs'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    borough = sa.Column(sa.String(80), unique=True, nullable=False)
    designation = sa.Column(sa.Enum('Inner', 'Outer', name='designation'))

    def __repr__(self):
        return '<Borough {}>'.format(self.borough)

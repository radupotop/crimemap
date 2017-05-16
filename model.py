import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql as pg

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


class ArticleContent(Base):
    __tablename__ = 'article_content'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    title = sa.Column(sa.Text())
    subtitle = sa.Column(sa.Text())
    href = sa.Column(sa.Text())
    author = sa.Column(sa.String(255))
    content = sa.Column(sa.Text())
    aside = sa.Column(sa.Text())
    media = sa.Column(pg.JSONB()) #images, video in JSON format
    meta = sa.Column(pg.JSONB()) #tags, other stuff in JSON format
    published_datetime = sa.Column(sa.DateTime())
    scrape_datetime = sa.Column(sa.DateTime())
    index_hash = sa.Column(sa.String(64), sa.ForeignKey('article_index.hash'), unique=True, nullable=False)

    def __repr__(self):
        return '<ArticleContent {} with Title {}>'.format(self.index_hash, self.title)


class Source(Base):
    """
    News sources.
    """
    __tablename__ = 'sources'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255))
    base_url = sa.Column(sa.String(255))
    scrape_href = sa.Column(sa.String(255))
    plugin = sa.Column(sa.String(255))
    poll_interval = sa.Column(sa.Integer, default=3600)

    def __repr__(self):
        return '<Source {} with Href {}>'.format(self.name, self.scrape_href)


class Borough(Base):
    __tablename__ = 'boroughs'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    borough = sa.Column(sa.String(80), unique=True, nullable=False)
    designation = sa.Column(sa.Enum('Inner', 'Outer', name='designation'))

    def __repr__(self):
        return '<Borough {}>'.format(self.borough)

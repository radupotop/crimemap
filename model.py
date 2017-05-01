import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

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


class Borough(Base):
    __tablename__ = 'boroughs'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    borough = sa.Column(sa.String(80), unique=True, nullable=False)
    designation = sa.column(sa.Enum('Inner', 'Outer'))

    def __repr__(self):
        return '<Borough {}>'.format(self.borough)

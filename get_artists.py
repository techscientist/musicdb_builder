# for rukkus
# to install
# pip install requests
# pip install sqlalchemy
# pip install mysql-python

# hiphop
urls_to_crawl    =   ['http://digitaldreamdoor.com/pages/best_rap-artists.html']

from lxml import html
import requests
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    rank = Column(Integer)
    status   = Column(String(255))
    def __repr__(self):
        return "<Artist(title='%s', rank='%s')>" % (
                             self.title,self.rank)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

engine = create_engine('mysql://root:@localhost:3306/rukkus', echo=False)

# create the table defined above
Base.metadata.create_all(engine)

# define a persistent connection
Session = sessionmaker(bind=engine)
session = Session()

for url in urls_to_crawl:
    body = requests.get(url).content
    tree = html.fromstring(body)
    artist_list = tree.xpath('//td/div[@class="list"]//span')
    for artist in artist_list:
        title = artist.tail.strip()
        print "title: (" + title + ')'
        rank = artist.text_content().replace('.','')
        print "rank: (" + rank + ')'
        insert = get_or_create(session, Artist, title=title)
        insert.rank = rank
        session.commit

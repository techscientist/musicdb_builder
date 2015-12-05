# for rukkus
# to install
# pip install requests
# pip install sqlalchemy
# pip install mysql-python
# pip install cssselect

# todo
# script breaks randomly cant find urllib3?

# some configuration
#useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'

use_cache = 1
headers = {
    'User-Agent': useragent,
}

from lxml import html
import requests
import base64
import os.path
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import TEXT
import re
import sys
import urllib

s = requests.Session()

# for debug
from pprint import pprint
from inspect import getmembers

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    rank = Column(Integer)
    status = Column(String(255))
    def __repr__(self):
        return "<Artist(title='%s', rank='%s')>" % (
                             self.title,self.rank)


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    lyrics = Column('lyrics', TEXT(charset='utf8'))
    year_released  = Column(Integer)
    link = Column(String(255))
    status = Column(String(255))
    album_id = Column(Integer)
    def __repr__(self):
        return "<Song(title='%s', lyrics='%s')>" % (
                             self.title,self.lyrics)

class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    year = Column(Integer)
    link = Column(String(255))
    status = Column(String(255))
    artist_id = Column(Integer)
    def __repr__(self):
        return "<Song(title='%s', lyrics='%s')>" % (
                             self.title,self.lyrics)

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

# get the next job
db = session.query(Song).filter(Song.status == None).first();

def cache_or_fetch(url):
    # handle caching
    encoded = base64.b64encode(url).replace('/','')
    #encoded = encoded[:-10]
    if os.path.exists('cache/' + encoded) and use_cache:
        print "from file %s" % encoded.encode('utf-8')
        f = open('cache/' + encoded,'r')
        text = f.read()
    else:
        print "from url"
        page = s.get(url, headers=headers)
        f = open('cache/' + encoded,'w')
        text = page.text
        text = text.encode('utf8')
        f.write(text)
    return text

url = db.link

print "fetching lyrics for", db.title, url

# parse first page
text = cache_or_fetch(url)

tree = html.fromstring(text)
lyrics = tree.xpath('//div[@id="lyrics"]')
lyric_tree = lyrics[0]
div = lyric_tree.find('ul')
if div:
    div.getparent().remove(div)

lyrics = lyrics[0].text_content()

db.lyrics = lyrics.encode('utf8')
db.status = 'done'
session.commit()
os.system("python get_song_to_lyrics.py")




# for rukkus
# to install
# pip install requests
# pip install sqlalchemy
# pip install mysql-python
# pip install cssselect

# todo
# script breaks randomly missing urllib3?

# some configuration
#useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'
base_search_url = 'http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s='
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
db = session.query(Artist).filter(Artist.status == None).first();

url = base_search_url+urllib.pathname2url(db.title)

def cache_or_fetch(url):
    # handle caching
    encoded = base64.b64encode(url).replace('/','')
    if os.path.exists('cache/' + encoded) and use_cache:
        print "from file %s" % encoded.encode('utf-8')
        f = open('cache/' + encoded,'r')
        text = f.read()
    else:
        print "from url"
        page = s.get(url, headers=headers)
        f = open('cache/' + encoded,'w')
        text = page.text
        text = text.encode('utf8');
        f.write(text)
    return text

def get_text_before(element):
    for item in element.xpath("preceding-sibling::*/text()|preceding-sibling::text()"):
        item = item.strip()
        if item:
            yield item

def get_text_after(element):
    for item in element.xpath("following-sibling::*/text()|following-sibling::text()"):
        item = item.strip()
        if item:
            yield item

print "searching for", db.title
print "URL:",url

# parse first page
text = cache_or_fetch(url)

tree = html.fromstring(text)
search_results = tree.xpath('//table[@class="table_as_list haspicture"]/tbody/tr/td/span[@class="low_profile"]')
for result in search_results:
    # TODO is this efficient ?
    result_type = result.text_content();
    if 'artist' in result_type:
        try:
            artist_link = result.xpath("preceding::a[@href]")[-1].get("href");
            artist_name = result.xpath("preceding::a[@href]")[-1].text_content()
            if artist_name.lower() == db.title.lower() or artist_name.lower().replace('.','') == db.title.lower().replace('.',''):
                # download artist result page
                artist_result_page = cache_or_fetch(artist_link)
                tree2 = html.fromstring(artist_result_page)
                album_list = tree2.xpath('//table[@class="table_as_list hasrank"]/tbody/tr/td')
                for album in album_list:
                    if '[' in album.text_content() and ']' in album.text_content():
                        album_name = album.find("a").text_content()
                        album_link  =   album.find("a").get('href')
                        m = re.search(r"\[([A-Za-z0-9_]+)\]", album_name)
                        album_year = '0'
                        if m:
                            year  = m.group(1)
                            if year.isdigit():
                                album_year = year

                        album_name = album_name.replace(' ['+str(album_year)+']','')
                        insert = get_or_create(session, Album,
                                               artist_id=db.id,
                                               title=album_name.strip().encode('utf-8'),
                                               year=album_year.encode('utf-8'),
                                               link=album_link.encode('utf-8'))

                db.status = 'done'
                session.commit()
                break
            # just in case we didnt find an artist
            db.status = 'done'
            session.commit()
            break
        except IndexError:
            print "not found"
# run itself again
os.system("python get_artist_to_albums.py")



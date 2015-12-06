from django.core.management.base import BaseCommand, CommandError
from django.db import models
import sys
sys.path.append("/Users/tty/workspace/musicdb_builder")
import json
from lxml import html
import requests
import re
import sys
import urllib
import base64
import os.path

# artist fetcher
urls_to_crawl = ['http://digitaldreamdoor.com/pages/best_rap-artists.html']
# words to ignore when counting appearances
stopwords = ['it\'s','you\'re','they','she','i\'m','you','i','a','about','and','an','are','as','at','be','by','com','for','from','how','in','is','it','of','on','or','that','the','this','to','was','what','when','where','who','will','with','the','www']
base_path = '/Users/tty/workspace/musicdb_builder/';
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'
# album, song and lyrics database
base_search_url = 'http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s='
# should we check if we have a cached version of the page
use_cache = 1
headers = {
    'User-Agent': useragent,
}

from musicdb.models import Song, Keyword, Artist, Album, Keyword

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)

    def get_or_create(self,model, **kwargs):
        instance = model.objects.filter(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            model.add(instance)
            model.save()
            return instance

    def cache_or_fetch(self,url):
        # handle caching
        encoded = base64.b64encode(url).replace('/','')
        if os.path.exists(base_path+'cache/' + encoded) and use_cache:
            print "from file %s" % encoded.encode('utf-8')
            f = open(base_path+'cache/' + encoded,'r')
            text = f.read()
        else:
            print "from url"
            page = s.get(url, headers=headers)
            f = open(base_path+'cache/' + encoded,'w')
            text = page.text
            text = text.encode('utf8');
            f.write(text)
        return text


    def analyze(self):
        db_songs = Song.objects.all()

        for song in db_songs:
            wordcount={}
            if song.lyrics:
                for word in song.lyrics.split():
                    if word.lower() not in stopwords and len(word) > 2:
                        if word not in wordcount:
                            wordcount[word] = 1
                        else:
                            wordcount[word] += 1
                print "."
                for key, value in wordcount.iteritems():
                    k = Keyword(term=key,appearances=value,song=song)
                    k.save()

    def get_artists(self):

        for url in urls_to_crawl:
            body = requests.get(url).content
            tree = html.fromstring(body)
            artist_list = tree.xpath('//td/div[@class="list"]//span')
            for artist in artist_list:
                title = artist.tail.strip()
                #print "title: (" + title + ')'
                rank = artist.text_content().replace('.','')
                #print "rank: (" + rank + ')'
                instance = self.get_or_create(Artist,title=title)
                instance.rank = rank
                instance.save()

    def get_artist_to_albums(self):
        # get the next job
        db = Artist.objects.filter(status=None).first();
        if db:
            url = base_search_url+urllib.pathname2url(db.title)
            print "searching for", db.title
            print "URL:",url
        else:
            print "no pending artists"
        text = self.cache_or_fetch(url)

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
                        artist_result_page = self.cache_or_fetch(artist_link)
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
                                insert = self.get_or_create(Album,
                                                            artist_id=db.id,
                                                            title=album_name.strip().encode('utf-8'),
                                                            year=album_year.encode('utf-8'),
                                                            link=album_link.encode('utf-8'))

                        db.status = 'done'
                        db.save()
                        break
                    # just in case we didnt find an artist
                    db.status = 'done'
                    session.save()
                    break
                except IndexError:
                    print "not found"

    def get_album_to_songs(self):
        db = Album.objects.filter(status=None).first();
        url = db.link

        print "fetching songs for", db.title, url


        # parse first page
        text = self.cache_or_fetch(url)

        tree = html.fromstring(text)
        search_results = tree.xpath('//tr[@itemtype="http://schema.org/MusicRecording"]')
        #print search_results
        for result in search_results:

            print "NOW IN"
            # TODO is this efficent ?
            song_title = result.find('td[2]').text_content()
            if 'lyrics' in song_title:
                song_title = song_title.split(' lyrics')[0]
                song_link  =  result.find('td[2]').find("a").get('href')
                print song_title
                print song_link
                insert = self.get_or_create(Song,
                                                       title=song_title.strip().encode('utf-8'),
                                                       link=song_link.encode('utf-8'),
                                                       album_id=db.id)

        # run itself again
        db.status = 'done'
        db.save()

    def get_song_to_lyrics(self):
        db = Song.objects.filter(status=None).first();

        url = db.link

        print "fetching lyrics for", db.title, url

        # parse first page
        text = self.cache_or_fetch(url)

        tree = html.fromstring(text)
        lyrics = tree.xpath('//div[@id="lyrics"]')
        lyric_tree = lyrics[0]
        div = lyric_tree.find('ul')
        if div:
            div.getparent().remove(div)

        lyrics = lyrics[0].text_content()

        db.lyrics = lyrics.encode('utf8')
        db.status = 'done'
        db.save()


    def handle(self, *args, **options):
        #self.get_artists()
        #self.get_artist_to_albums()
        #self.get_album_to_songs()
        self.get_song_to_lyrics()
        #self.analyze()
        self.stdout.write("Finished", ending='')
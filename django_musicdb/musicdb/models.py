from django.db import models

# Create your models here.

class Artist(models.Model):
    title = models.CharField(max_length=255)
    rank = models.IntegerField()
    status = models.CharField(max_length=255)

    objects =   models.Manager()
    def __str__(self):
        return "%s %s %s" % (self.title, self.rank, self.status)

class Album(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    link = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, default=1, null=True, related_name='albums')
    def __str__(self):
        return "%s %s %s %s %s" % (self.title, self.year, self.link, self.status)

class Song(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField(null=True)
    link = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True)
    keyword_dict    =   models.TextField(null=True)
    album = models.ForeignKey(Album, default=1, null=True, related_name='songs')
    def __str__(self):
        return "%s %s %s %s %s" % (self.title, self.lyrics, self.year, self.link, self.status, self.keyword_dict)

class Keyword(models.Model):
    term = models.CharField(max_length=255)
    appearances = models.IntegerField()
    song = models.ForeignKey(Song, default=1, null=True, related_name='keywords')
    def __str__(self):
        return "%s %s %s" % (self.term, self.appearances)
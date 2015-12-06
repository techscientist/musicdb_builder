from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from musicdb.models import Artist, Song, Album


def artist(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        raise Http404("Artist could not be found!")

    return render_to_response('artist.html', {'artist': artist })

def report(request):
    stats = {}
    #,,'2013','2012','2011','2010','2009','2008','2007','2006','2005'
    years = ['2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005']
    for ye in years:
        stats[ye] = []
        print ye
        year_stats = {  }

        try:
            albums = Album.objects.filter(year=ye)
            for album in albums:
                songs = Song.objects.filter(album_id=album.id)
                # compute stats
                for song in songs:
                    for keyword in song.keywords.order_by('-appearances')[:20]:
                        if keyword.term not in year_stats:
                            year_stats[keyword.term] = keyword.appearances
                        else:
                            year_stats[keyword.term] += keyword.appearances

            for word in year_stats:
                obj = { 'term'    :   word, 'count'    :   year_stats[word] }
                stats[ye].append(obj)

        except Artist.DoesNotExist:
            raise Http404("Songs could not be found!")
        #stats[str(ye)] = year_stats


    return render_to_response('report.html', {'stats': stats })

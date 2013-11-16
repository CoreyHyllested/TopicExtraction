'''
Created on Sep 21, 2013

@author: cllyon
'''

#import cProfile

import requests  # @UnresolvedImport
from collections import Counter

API_KEY = "YOUR_KEY"
NUM_TO_KEEP = 10
LFM_API_URL = "http://ws.audioscrobbler.com/2.0/"


def _api_call(params):
    return requests.get(LFM_API_URL, params=params).json()


def get_artist_info(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=Cher&
    api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    params = {"method": "artist.getinfo",
              "artist": artist_name,
              "api_key": API_KEY,
              "format": "json"}
    o = _api_call(params)
    return o['artist']['bio']['summary']


def get_top_tags_for_artist(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=cher&
    api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    tags = Counter()
    params = {"method": "artist.gettoptags",
              "artist": artist_name,
              "api_key": API_KEY,
              "format": "json"}
    o = _api_call(params)
    if 'toptags' in o and 'tag' in o['toptags']:
        for t in o['toptags']['tag']:
            try:
                tags[normtag(t['name'])] += int(t['count'])
            except:
                pass
    return tags


def get_top_albums_for_artist(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=cher&
    api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    albums = []
    params = {"method": "artist.gettopalbums",
              "artist": artist_name,
              "api_key": API_KEY,
              "format": "json"}
    o = _api_call(params)
    for t in o['topalbums']['album']:
        albums.append(t['name'])
    return albums


def get_top_tracks_for_artist(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=cher&
    api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    tracks = []
    params = {"method": "artist.gettoptracks",
              "artist": artist_name,
              "api_key": API_KEY,
              "format": "json"}
    o = _api_call(params)
    for t in o['toptracks']['track']:
        tracks.append(t['name'])
    return tracks


def get_top_album_tags_for_artist(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=album.gettoptags&
        artist=radiohead&album=the%20bends&
        api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    tags = Counter()
    for album_name in get_top_albums_for_artist(artist_name):
        params = {"method": "album.gettoptags",
              "artist": artist_name,
              "album": album_name,
              "api_key": API_KEY,
              "format": "json"}
        o = _api_call(params)
        if 'tag' in o['toptags']:
            for t in o['toptags']['tag']:
                try:
                    tags[normtag(t['name'])] += int(t['count'])
                except:
                    pass
    return tags


def get_top_track_tags_for_artist(artist_name):
    '''
    http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&
        artist=radiohead&track=the%20bends&
        api_key=5aa8bf757286ea2e0d3caf9657744549&format=json
    '''
    tags = []
    for track_name in get_top_tracks_for_artist(artist_name):
        params = {"method": "track.gettoptags",
              "artist": artist_name,
              "track": track_name,
              "api_key": API_KEY,
              "format": "json"}
        o = _api_call(params)
        for t in o['toptags']['tag']:
            try:
                tags[normtag(t['name'])] += int(t['count'])
            except:
                pass
    return tags


def normtag(t):
    return str(t).lower().replace(" ", "_")


def top_last_fm_tags(artist_name):
    tags = get_top_tags_for_artist(artist_name)
    tags += get_top_album_tags_for_artist(artist_name)
    tags += get_top_track_tags_for_artist(artist_name)
    return tags.most_common(NUM_TO_KEEP)


if __name__ == "__main__":
    tags = top_last_fm_tags("sting")
    print tags
    print get_artist_info("sting")

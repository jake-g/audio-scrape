#!/usr/local/bin/python
from __future__ import unicode_literals

import re
import sys
import youtube_dl
import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus

# TODO setup.py
# TODO Spotify search playlist, song, album
# TODO Soundcloud searching too


# Defaults
default_path = '/Users/jake/Google Drive/Music/Dj/tst/'
# Settings for youtube-dl
dl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': default_path + '%(title)s.%(ext)s',
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'MetadataFromTitle',
            'titleformat': "%(artist)s - %(title)s"
        },
        {
            'key': 'FFmpegMetadata',
        },
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0'
        },
        {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False
        }
    ]
}


class logger(object):
    def debug(self, msg):
        # pass
        print(msg)

    def warning(self, msg):
        # pass
        print(msg)

    def error(self, msg):
        print(msg)


def download_playlist(playlist):
    # must be txt file with link per line
    print 'Downloading List...\n'
    with open(playlist) as f:
        urls = [urls.strip() for urls in f]
        count = len(urls)
        for i, url in enumerate(urls):
            print '(file %d/%d)' % (i, count)
            download_track(i)


def download_track(url):
    dl_opts[u'logger'] = logger()
    dl_opts[u'progress_hooks'] = [hook]
    if 'soundcloud.com' in url:
        dl_opts[u'postprocessors'][0][u'titleformat'] = "%(uploader)s - %(title)s"

    with youtube_dl.YoutubeDL(dl_opts) as ydl:
        ydl.download([url])


def hook(d):
    if d['status'] == 'finished':
        path, artist, track, ext, size = get_info(d)
        print '[saved]'
        print '\tartist:\t', artist
        print '\ttrack:\t', track
        print '\text:\t', ext
        print '\tsize:\t', size
        print '\tpath:\t', path


def get_info(data):
    # use with hook
    size = data[u'_total_bytes_str']
    path, filename = os.path.split(data[u'filename'])
    artist, name = filename.split(' - ')
    track, ext = name.split('.')
    return [path, artist, track, ext, size]


def valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def extract_videos(html):
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def process_search(query):
    search = quote_plus(query)
    available = search_videos(search)
    if not available:
        print 'No results found matching your query.'
        sys.exit()

    print "Search Results:"
    print '\n'.join(list_movies(available))
    choice = ''  # pick choice
    while choice.strip() == '':
        choice = raw_input('Pick one: ')
        title, video_link = available[int(choice)]
        download_track('http://www.youtube.com/' + video_link)


def search_videos(query):
    print 'Searching...'
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())


def help_text():
    print '\nInput Query:\n' \
          ' URL (valid if url to youtube or soundcloud track/playlist/set)\n' \
          ' Link File (a path to a .txt containing valid URLs)\n' \
          ' Search (songname/lyrics/artist or other)\n' \
          ' Type reddit to browse by subreddit\n'


def main():
    # TODO add arg parser arg: choose path, help, reddit, update (praw and youtubedl)

    # Get Query
    if len(sys.argv) == 2:  # input argument
        query = sys.argv[1]
    else:  # ask for input
        help_text()
        # query = str(raw_input('Query:\n> '))
        # query = 'https://youtu.be/szTrH6XgA_M'
        query = 'https://soundcloud.com/thissoundgoesaround/50-cent-many-men-tnv-reflip'

    # Process Query
    if valid_url(query):  # track
        download_track(query)
    elif '.txt' in query:  # playlist
        download_playlist(query)
    else:
        process_search(query)  # search


if __name__ == '__main__':
    main()
    print 'Done'

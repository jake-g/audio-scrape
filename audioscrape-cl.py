#!/usr/local/bin/python
__author__ = 'jake'


import re
import sys
import subprocess
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus


# Defaults
default_playlist = 'urls.txt'
default_path = '/Users/jake/Google Drive/Music/Dj/unsorted/'

def download_playlist(playlist):
    print 'Downloading List...\n'
    with open(playlist) as f:
        urls = [urls.strip() for urls in f]
        count = len(urls)
        current = 1
        for url in urls:
            print '(file %d/%d)' % (current, count)
            download_track(url)
            current += 1


# Downloads to temp directory
def download_track(url, path=''):
    if path == '':   # default
        path = default_path

    print 'Downloading...'
    print '[url] %s' % url
    print '[path] %s' % path

    command = [
        'youtube-dl',                   # command
        '-x', '-f bestaudio/best',      # best quality audio
        '--embed-thumbnail',            # embed art
        '-o', path + '%(title)s.%(ext)s',    # output path
        url ]

    subprocess.call(command)


def valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
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


def search_videos(query):
    print 'Searching...'
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())


def main():
    query = sys.argv[1]

    # Playlist
    if '.txt' in query:     # must be txt file with link per line
        download_playlist(query)

    # Track
    elif valid_url(query):      # single track
        download_track(query)

    # Search
    else:
        search = quote_plus(query)
        available = search_videos(search)
        if not available:
            print 'No results found matching your query.'
            sys.exit()

        print "Search Results:"
        print '\n'.join(list_movies(available))
        choice = ''                     # pick choice
        while choice.strip() == '':
            choice = raw_input('Pick one: ')
            title, video_link = available[int(choice)]
            download_track('http://www.youtube.com/' + video_link, path)

    print 'Finished'

if __name__ == '__main__':
    main()

#!/usr/local/bin/python
from __future__ import unicode_literals

import re
import subprocess
import sys
from urllib import quote_plus
from urllib2 import urlopen

from bs4 import BeautifulSoup

# TODO setup.py
# TODO Soundcloud searching too
# TODO add config file in setup that allows this to be set


# Defaults
default_path = '/Users/jake/Google Drive/Music/Dj/'

def download_playlist(playlist):
    print 'Downloading List...\n'
    with open(playlist) as f:
        urls = [urls.strip() for urls in f]
        count = len(urls)
        for i, url in enumerate(urls):
            print '\n(file %d/%d)' % (i, count)
            download_track(url)


def download_track(url, path=default_path):
    dl_options = \
    ['youtube-dl',
     'extract-audio',
     'audio-format mp3',
     'embed-thumbnail',
     'add-metadata',
     'metadata-from-title "%(artist)s - %(title)s"',
     'audio-quality 0',
     'output']

    filename = "'" + path + "%(title)s.%(ext)s" + "'"
    if 'soundcloud.com' in url:
        dl_options[5] = 'metadata-from-title "%(uploader)s - %(title)s"'

    cmd = ' --'.join(dl_options)
    proc = subprocess.Popen(' '.join([cmd, filename, url]), shell=True, stdout=subprocess.PIPE)
    print_status(proc)


def print_status(proc):
    while not proc.poll():
        status = proc.stdout.readline()
        if status:
            sys.stdout.write(status)
        else:
            break


def valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
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
          ' Search (songname/lyrics/artist or other)\n'


def main():

    # Get Query
    if len(sys.argv) == 2:  # input argument
        query = sys.argv[1]
    else:  # ask for input
        help_text()
        query = str(raw_input('Query:\n> '))

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

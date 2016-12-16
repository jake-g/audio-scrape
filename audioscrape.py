#!/usr/local/bin/python
from __future__ import unicode_literals, print_function

import re
import sys
import youtube_dl
import os
import eyed3
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
import argparse
import pprint


# hack for osx
reload(sys)
sys.setdefaultencoding('utf8')



# Defaults
PATH = '/Users/jake/Desktop/'
VERBOSITY = 0

# Settings for youtube-dl
dl_opts = {
    'format': 'bestaudio/best',
    'forcejson': True,
    'outtmpl': PATH + '%(title)s.%(ext)s',
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'MetadataFromTitle',
            'titleformat': "%(artist)s - %(title)s"
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
    def __init__(self):
        self.d = {}

    def info(self, msg):
        if VERBOSITY > 0:
            print(msg)
        pass

    def debug(self, msg):
        if VERBOSITY > 1:
            print(msg)
        pass

    def warning(self, msg):
        if VERBOSITY > 0:
            print(msg)
        pass

    def error(self, msg):
        print(msg)

    def status(self, msg):
        print(msg)
        # sys.stdout.write(msg)
        # sys.stdout.flush()




def download_playlist(playlist):
    # must be txt file with link per line
    print('Downloading List...\n')
    with open(playlist) as f:
        urls = [urls.strip() for urls in f]
        count = len(urls)
        for i, url in enumerate(urls):
            print('\n(line %d/%d)' % (i, count))
            print('[url]', url)
            try:
                if '#' not in url:
                    download_track(str(url))
            except:
                pass


def download_track(url):
    dl_opts[u'logger'] = logger()
    dl_opts[u'progress_hooks'] = [callback]
    log.status('[\033[91mFetching\033[00m] %s\n' % url)
    if 'soundcloud.com' in url:
        dl_opts[u'postprocessors'][0][u'titleformat'] = "%(uploader)s - %(title)s"
    with youtube_dl.YoutubeDL(dl_opts) as ydl:
        ydl.download([url])

    # write_metadata(log.d)
    log.status('\x1b[1A[\033[92mDownloaded\033[00m] %s\n' % (log.d[u'title']))
    print_info(log.d)


def callback(d):
    pprint.pprint(d)
    if d['status'] == 'downloading':
        pass

    if d['status'] == 'finished':
        d = get_info(d)  # update d
        log.status('\x1b[1A[\033[93mConverting\033[00m] %s\n' % (d[u'fname']))


def write_metadata(d):
    f, ext = os.path.splitext(d[u'filename'])
    filename = f + '.mp3'
    if os.path.isfile(filename):
        file = eyed3.load(filename)
        file.tag.title = d[u'title']
        file.tag.artist = d[u'artist']
        file.tag.save()
        d[u'filename'] = filename
    else:
        log.status('\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\n' % filename)


def get_info(d):
    # use with hook
    d[u'path'], d[u'fname'] = os.path.split(d[u'filename'])
    d[u'artist'], name = d[u'fname'].split(' - ')
    d[u'title'], d[u'ext'] = os.path.splitext(name)
    log.d = d
    return d


def print_info(d):
    log.info('[saved]\n\t'
             'artist:\t %s\n\t'
             'track:\t %s\n\t'
             'ext:\t %s\n\t'
             'size:\t %s\n\t'
             'path:\t %s'
             % (d[u'artist'], d[u'title'], d[u'ext'], d[u'_total_bytes_str'], d[u'path']))


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


def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def process_search(query):
    search = quote_plus(query)
    available = search_youtube(search)
    if not available:
        print('No results found matching your query.')
        sys.exit()

    print("Search Results:")
    print('\n'.join(list_movies(available)))
    choice = ''  # pick choice
    while choice.strip() == '':
        choice = raw_input('Pick one: ')
        print('')
        title, video_link = available[int(choice)]
        download_track('http://www.youtube.com/' + video_link)


def search_youtube(query):
    print('Searching...')
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_links(response.read())


def help_text():
    print('\nInput Query:\n' \
          ' URL (valid if url to youtube or soundcloud track/playlist/set)\n' \
          ' Link File (a path to a .txt containing valid URLs)\n' \
          ' Search (songname/lyrics/artist or other)\n')


def main(args):
    # Get Query
    PATH = args.path
    if args.link:  # input argument
        query = args.link
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", "-l", type=str, help="url to download")
    parser.add_argument("--path", "-p", default=PATH, type=str, help="download path")
    args = parser.parse_args()
    log = logger()

    main(args)

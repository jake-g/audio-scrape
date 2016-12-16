#!/usr/local/bin/python
from __future__ import unicode_literals, print_function

import argparse
import re
import sys
from urllib import quote_plus
from urllib2 import urlopen

import youtube_dl
from bs4 import BeautifulSoup

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
    def debug(self, msg):
        if VERBOSITY > 0:
            print(msg)
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


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
    print('[\033[91mFetching\033[00m] %s\n' % url)
    if 'soundcloud.com' in url:
        dl_opts[u'postprocessors'][0][u'titleformat'] = "%(uploader)s - %(title)s"
    with youtube_dl.YoutubeDL(dl_opts) as ydl:
        ydl.download([url])


def callback(d):
    # pprint.pprint(d)

    if d['status'] == 'finished':
        print('\x1b[1A[\033[92mSaving\033[00m] %s' % (d[u'filename']))


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


def list_links(links):
    for idx, (title, _) in enumerate(links):
        yield '[{}] {}'.format(idx, title)


def process_search(query):
    search = quote_plus(query)
    available = search_youtube(search)
    if not available:
        print('No results found matching your query.')
        sys.exit()

    print("Search Results:")
    print('\n'.join(list_links(available)))
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

    main(args)

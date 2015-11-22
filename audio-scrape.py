# TODO setup.py
# TODO add config file in setup that allows path to be set
# TODO batch option (see -a ytdl opt)
# TODO support youtube-dl -U to update command
# TODO run thru beet tag (use --exec CMD ytdl)
# TODO if in playlist, then add this to tag: %(playlist_title)s-%(playlist_index)s
# TODO Spotify playlist
__author__ = 'jake'


import os
import re
import sys
import subprocess
import shutil
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus

# TODO use extract to name inputed url from audio-crape original download
# TODO have it return playlists
# TODO Soundcloud searching too




# Defaults
default_playlist = 'urls.txt'
default_path = '/Users/jake/Google Drive/Music/Dj/unsorted/'
default_path = "C:\Users\jake\Google Drive\\"


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
def download_track(url):
    path = str(raw_input('Save Path (blank for default):\n> '))

    if path == '':   # default
        path = default_path

    print 'Downloading...\n'
    print '[url] %s' % url
    print '[path] %s' % path

    command = [
        'youtube-dl',                   # command
        '-x', '-f bestaudio/best',      # best quality audio
        '--embed-thumbnail',            # embed art
        # '--add-metadata',                # scrape metadata
        # TODO Fix metadata
        # DOESNT WORK WITH PLAYLIST! '--metadata-from-title',
        # '%(artist)s - %(title)s',
        '-o', path + '%(title)s.%(ext)s',    # output path
        url ]

    # TODO print '[saved] %s' % trackname
    subprocess.call(command)


# TODO delete this when you have a way to extract track names
# def process_track(tmp, path):
#     playlist = os.listdir(tmp)
#     for track in playlist:
#         shutil.move(os.path.join(tmp,track), os.path.join(path,track))    # move from tmp
#         print '[saved] %s' % track
#     shutil.rmtree(tmp)          # delete temp


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
    """
    Parses given html and returns a list of (Title, Link) for
    every movie found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def search_videos(query):
    """
    Searchs for videos given a query
    """
    print 'Searching...'
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())

def main():

    # Query
    print '\nInput Query:\n' \
          ' URL (valid if url to youtube or soundcloud track/playlist/set)\n' \
          ' Link File (a path to a .tx containing valid URLs)\n' \
          ' Search (songname/lyrics/artist or other)\n'
    query = str(raw_input('Query:\n> '))

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

        print "Found:", '\n'.join(list_movies(available))
        choice = ''                     # pick choice
        while choice.strip() == '':
            choice = raw_input('Pick one: ')

            title, video_link = available[int(choice)]
            download_track('http://www.youtube.com/' + video_link)


    print '\nFinished!'

if __name__ == '__main__':
    main()


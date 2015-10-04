# TODO setup.py
# TODO add config file in setup that allows path to be set
# TODO batch option (see -a ytdl opt)
# TODO support youtube-dl -U to update command
# TODO run thru beet tag (use --exec CMD ytdl)
# TODO if in playlist, then add this to tag: %(playlist_title)s-%(playlist_index)s

__author__ = 'jake'
# requre youtube-dl

import subprocess
import os
import sys
import shutil
import easygui

# Downloads to temp directory
def download_track(url, path):
    print 'Downloading...\n'
    print '[url] %s' % url
    print '[path] %s' % path
    tmp = os.path.join(path,'tmp/')

    command = [
        'youtube-dl',                   # command
        '-x', '-f bestaudio/best',      # best quality audio
        '--embed-thumbnail',            # embed art
        #'--add-metadata',                # scrape metadata
        '--metadata-from-title',
        '%(artist)s - %(title)s',
        '-o', tmp + '%(title)s.%(ext)s',    # output path
        url ]
                                   # url
    subprocess.call(command)
    process_track(tmp, path)


def process_track(tmp, path):
    playlist = os.listdir(tmp)
    for track in playlist:
        shutil.move(os.path.join(tmp,track), os.path.join(path,track))    # move from tmp
        print '[saved] %s' % track
    shutil.rmtree(tmp)          # delete temp


def main():
    path = raw_input('Save Path (leave blank for path open gui) : ')
    if path == '':  # path gui
        path = easygui.diropenbox()


    url = str(raw_input('Track URL (leave blank for input list: '))
    if 'www' not in url:   # input file, multiple tracks
        with open(url) as f:
            urls = [urls.strip() for urls in f]
            count = len(urls)
            current = 1
            for url in urls:
                print url
                print '(file %d/%d)' % (current, count)
                download_track(url, path)
                current += 1

    else:       # single track
        download_track(url, path)

    print '\n Finished!'

if __name__ == '__main__':
    status = main()
    sys.exit(status)
# TODO setup.py
# TODO add config file in setup that allows path to be set
# TODO support youtube-dl -U to update command

__author__ = 'jake'
# requre youtube-dl

import subprocess
import os
import sys
import shutil
import easygui

# Downloads to temp directory
def download_track(url, path):
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
    url = easygui.enterbox(msg='Track URL: ', title='Input URL', default='', strip=True)
    path = easygui.diropenbox() # '/Users/jake/Desktop/audio-scrape/'
    try:
        print '\nScraping %s to %s...\n' % (url, path)
    except:
        print 'URL or path not valid...\nQuitting!'
        exit()
    download_track(url, path)
    print '\n Finished!'


if __name__ == '__main__':
    status = main()
    sys.exit(status)
# TODO -s or something to display sources (youtube-dl --list-extractors will list scrapers)
# TODO add script options (not the same as ytdl ones) (-q quiet -v verbose -h help -p path)
# TODO add config file in setup that allows path to be set
# TODO batch option (see -a ytdl opt)
# TODO support youtube-dl -U to update command
# TODO run thru beet tag (use --exec CMD ytdl)
# TODO if in playlist, then add this to tag: %(playlist_title)s-%(playlist_index)s


'''
USEFUL OPTIONS
~FILE IO~
-a, --batch-file FILE            File containing URLs to download ('-' for stdin)
-o, --output TEMPLATE            Output filename template. Use %(title)s to get the title, %(uploader)s for the uploader name, %(uploader_id)s for the uploader
                                 nickname if different, %(autonumber)s to get an automatically incremented number, %(ext)s for the filename extension, %(format)s for
                                 the format description (like "22 - 1280x720" or "HD"), %(format_id)s for the unique id of the format (like YouTube's itags: "137"),
                                 %(upload_date)s for the upload date (YYYYMMDD), %(extractor)s for the provider (youtube, metacafe, etc), %(id)s for the video id,
                                 %(playlist_title)s, %(playlist_id)s, or %(playlist)s (=title if present, ID otherwise) for the playlist the video is in,
                                 %(playlist_index)s for the position in the playlist. %(height)s and %(width)s for the width and height of the video format.
                                 %(resolution)s for a textual description of the resolution of the video format. %% for a literal percent. Use - to output to stdout.
                                 Can also be used to download to a different directory, for example with -o '/my/downloads/%(uploader)s/%(title)s-%(id)s.%(ext)s' .
--autonumber-size NUMBER         Specify the number of digits in %(autonumber)s when it is present in output filename template or --auto-number option is given

--exec CMD                       Execute a command on the file after downloading, similar to find's -exec syntax. Example: --exec 'adb push {} /sdcard/Music/ && rm
                                 {}'
The special sequences have the format %(NAME)s.
The current default template is %(title)s-%(id)s.%(ext)s.


uploader: The sequence will be replaced by the nickname of the person who uploaded the video.
upload_date: The sequence will be replaced by the upload date in YYYYMMDD format.
title: The sequence will be replaced by the video title.
ext: The sequence will be replaced by the appropriate extension (like flv or mp4).
playlist: The sequence will be replaced by the name or the id of the playlist that contains the video.
playlist_index: The sequence will be replaced by the index of the video in the playlist padded with leading zeros according to the total length of the playlist.
format_id: The sequence will be replaced by the format code specified by --format.
duration: The sequence will be replaced by the length of the video in seconds.


~MODES~
-q, --quiet                      Activate quiet mode
--no-warnings                    Ignore warnings
--newline                        Output progress bar as new lines
--no-progress                    Do not print progress bar
--console-title                  Display progress in console titlebar
-v, --verbose                    Print various debugging information


~FORMAT~
* use '-f bestaudio/best'
-f, --format FORMAT              Video format code, see the "FORMAT SELECTION" for all the info
-x, --extract-audio              Convert video files to audio-only files (requires ffmpeg or avconv and ffprobe or avprobe)
--audio-format FORMAT            Specify audio format: "best", "aac", "vorbis", "mp3", "m4a", "opus", or "wav"; "best" by default
--audio-quality QUALITY          Specify ffmpeg/avconv audio quality, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default
                                 5)

~METADATA~
--embed-thumbnail                Embed thumbnail in the audio as cover art
--add-metadata                   Write metadata to the video file
--metadata-from-title FORMAT     Parse additional metadata like song title / artist from the video title. The format syntax is the same as --output, the parsed
                                 parameters replace existing values. Additional templates: %(album)s, %(artist)s. Example: --metadata-from-title "%(artist)s -
                                 %(title)s" matches a title like "Coldplay - Paradise"

'''


__author__ = 'jake'
# requre youtube-dl

from subprocess import call
import os
import sys
import shutil


path = '/Users/jake/Desktop/audio-scrape/'


# Downloads to temp directory
def download_track(url):
    tmp = os.path.join(path,'tmp/')

    command = [
        'youtube-dl',                   # command
        '-x', '-f bestaudio/best',      # best quality audio
        '--embed-thumbnail',            # embed art
        '--add-metadata',                # scrape metadata
        '--metadata-from-title',
        '%(artist)s - %(title)s',
        '-o', tmp + '%(title)s.%(ext)s',    # output path
        url ]
                                   # url
    call(command)
    return tmp

def process_track(tmp):
    playlist = os.listdir(tmp)
    for track in playlist:
        shutil.move(os.path.join(tmp,track), os.path.join(path,track))    # move from tmp
        print '[saved] %s' % track

    shutil.rmtree(tmp)          # delete temp


def main():
    print 'Scraping audio to %s...\n' % path

    url = 'www.youtube.com/watch?v=wQlHYvy0xdU' #'https://soundcloud.com/futureclassic/charles-murdoch-frogs-feat-ta-ku-wafia-hak'  #raw_input("Stream URL: ")    # input URL from the site you'd like to scrape

    dl = download_track(url)
    process_track(dl)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
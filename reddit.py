import praw
from sys import argv
import os
import sys
import optparse


# TODO add a way to list all subreddits (scrape from playlister.io
# filter and download youtube or soundcloud links
def download(url):
    print url


def git_reddit(sub, links):
    # get submisisons from reddit
    count = 0
    r = praw.Reddit(user_agent='Playlist Builder')
    for post in r.get_subreddit(sub).get_hot(limit = links):
        if (count > int(links)):
            print "Downloaded %d links" % count
            sys.exit("Done...")
        download(str(post.url))
        count += 1


def main():
    path = '/Users/jake/Desktop/rplaylist_cache/'
    sub = raw_input('Subreddit (? \n >  ')
    links = raw_input('How Many? \n >  ')
    if not os.path.exists(path):   # make cache folder
        os.makedirs(path)

    git_reddit(sub, links)

if __name__ == '__main__':
    main()
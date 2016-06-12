#!/usr/local/bin/python

import praw
import audioscrape

reddit_cache = './reddit_cache/'


def download_reddit(sub, sort, n_links=10):
    posts = get_posts(sub, sort)
    for i, post in enumerate(posts):
        link = str(post.url)
        if 'youtu' in link or 'soundc' in link:
            print "\n[Link %d] : %s" % (i + 1, link)
            audioscrape.download_track(link, reddit_cache)
        if i is n_links:
            break
    print "Downloaded %d links" % i


def get_posts(sub, sort):
    n = None
    r = praw.Reddit(user_agent='Playlist Builder')
    posts = []
    if sort is 'hot':
        posts = r.get_subreddit(sub).get_hot(limit=n)
    elif sort is 'new':
        posts = r.get_subreddit(sub).get_new(limit=n)
    elif sort is 'rising':
        posts = r.get_subreddit(sub).get_rising(limit=n)
    elif sort is 'top':
        posts = r.get_subreddit(sub).get_top(limit=n)
    elif sort is 'all':
        posts = r.get_subreddit(sub).get_top_from_all(limit=n)
    elif sort is 'day':
        posts = r.get_subreddit(sub).get_top_from_day(limit=n)
    elif sort is 'hour':
        posts = r.get_subreddit(sub).get_top_from_hour(limit=n)
    elif sort is 'month':
        posts = r.get_subreddit(sub).get_top_from_month(limit=n)
    elif sort is 'week':
        posts = r.get_subreddit(sub).get_top_from_week(limit=n)
    elif sort is 'year':
        posts = r.get_subreddit(sub).get_top_from_year(limit=n)
    else:
        print '[Error] Invalid sorting filter'

    return posts


if __name__ == '__main__':
    # TODO Add arg parsing and main()
    # TODO Add playback (queue next songs while playback is going)
    # number_of_links = 20
    subreddit = 'futurebeats'
    sort = 'hot'
    download_reddit(subreddit, sort, 20)
    # download_reddit(subreddit, sort, number_of_links)

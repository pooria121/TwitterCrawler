#!/usr/bin/python
# -*- coding: utf-8 -*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy.parsers import *
from tweepy import Stream, API
import json
import tweepy
from pymongo import MongoClient
import argparse
import ConfigParser


# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('crawler.cfg')

# Reading Twitter API settings from config file
consumer_key = config.get('twitter', 'consumer_key')
consumer_secret = config.get('twitter', 'consumer_secret')
access_token = config.get('twitter', 'access_token')
access_secret = config.get('twitter', 'access_secret')
language = config.get('twitter', 'language')


#Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
posts = db[config.get('mongodb', 'schema')]


class TweetStreamListener(StreamListener):
    """ A listener that handles the  recived tweets
        using on_status method"""

    def save(self, status):
        user_json = status.user.__getstate__()
        user_json['created_at'] = str(status.user.created_at)
        user_json['type'] = 'user'
        place_json = None
        if status.place != None:
            place_json = status.place.__getstate__()
            if status.place.bounding_box != None:
                place_json['bounding_box'] = \
                    status.place.bounding_box.__getstate__()

        doc = {
            'type': 'Tweet',
            'contributors': status.contributors,
            'coordinates': status.coordinates,
            'created_at': str(status.created_at),
            'entities': status.entities,
            'favorite_count': status.favorite_count,
            'favorited': status.favorited,
            'geo': status.geo,
            'id': status.id,
            'id_str': status.id_str,
            'in_reply_to_screen_name': status.in_reply_to_screen_name,
            'in_reply_to_status_id': status.in_reply_to_status_id,
            'in_reply_to_status_id_str': status.in_reply_to_status_id_str,
            'in_reply_to_user_id': status.in_reply_to_user_id,
            'in_reply_to_user_id_str': status.in_reply_to_user_id_str,
            'lang': status.lang,
            'place': place_json,
            'retweet_count': status.retweet_count,
            'retweeted': status.retweeted,
            'source': status.source,
            'source_url': status.source_url,
            'text': status.text,
            'truncated': status.truncated,
            'user': user_json,
            }

                    # print doc
                    # print status.user.__getstate__()

        print doc['id']
        posts.insert(doc)

    def on_status(self, status):
        """this method will handle and parse recieved tweets"""

        found = posts.find_one({'id': status.id})

        if hasattr(status, 'lang') and status.lang == language \
            and found == None:
            self.save(status)
        return True


def sample():
    '''Calling the sampling API provided by twitter.'''
    listener = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.sample()


def filter(query):
    '''Calling the streaming API provided by twitter and only track the
    keywords that are supplied from command-line by the user.'''
    listener = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.filter(track=query)


def search(query):
    '''Uses Twitter search API to search the keywords individually that are requested
    by the user from command-line.'''
    listener = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = API(auth)
    for term in query:
        print 'Searching for:' + term
        results = api.search(q=term, lang=language, result_type='mixed'
                             , include_entities=True, rpp=100)
        for status in results:
            found = posts.find_one({'id': status.id})
            if found == None:
                listener.save(status)


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='Download tweets from Twitter.com'
                                )
    parser.add_argument('query', metavar='Q', type=str, nargs='+',
                        help='query terms to be searched')

    parser.add_argument('--search', action='store_true',
                        help='perform search on the query')

    parser.add_argument('--sample', action='store_true',
                        help='Sample tweets using sampling API')

    parser.add_argument('--filter', action='store_true',
                        help='Getting stream of tweets and tracking the keywords'
                        )

    args = parser.parse_args()
    if args.search:
        search(args.query)
    elif args.sample:
        stream()
    elif args.filter:
        filter(args.query)

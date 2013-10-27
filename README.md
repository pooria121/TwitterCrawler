TwitterCrawler
==============

Generic Twitter crawler for crawling and storing tweets using Sample/Filter/Search APIs 
provided by Twitter into Mongodb database


Requirements
============


How to Use
==========
Poorias-iMac:TwitterCrawler pooria$ python twitter_crawler.py -h
      usage: twitter_crawler.py [-h] [--search] [--sample] [--filter] Q [Q ...]
      
      Download tweets from Twitter.com
      
      positional arguments:
        Q           query terms to be searched
      
      optional arguments:
        -h, --help  show this help message and exit
        --search    perform search on the query
        --sample    Sample tweets using sampling API
        --filter    Getting stream of tweets and tracking the keywords
        
        
        
For searching some keywords:
  Poorias-iMac:TwitterCrawler pooria$ python twitter_crawler.py --search topic1 topic2 topic3
  
For tracking some keywords like using stream API:
  Poorias-iMac:TwitterCrawler pooria$ python twitter_crawler.py --track topic1 topic2 topic3
  
For sampling recent tweets:
  Poorias-iMac:TwitterCrawler pooria$ python twitter_crawler.py --sample

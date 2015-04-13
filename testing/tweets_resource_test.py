import unittest
import json
import datetime

import sys
sys.path.append('/Users/renee/Projects/personal-projects/Pwitter')

from service import db
from service.models import Broadcaster2Follower, Tweet
from base_test import BaseTest, auth_headers



class TweetResourceTest(BaseTest):

    def test_view_tweets(self):
        r = self.app.get(
            '/tweets',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 2

        assert tweets[0]['username'] == 'trenton'
        assert tweets[0]['body'] == 'burning man'
        assert tweets[0]['date_created'] == "Fri, 02 Jan 2015 00:00:00 -0000"

        assert tweets[1]['username'] == 'reneighbor'
        assert tweets[1]['body'] == 'hello world'
        assert tweets[1]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"


    def test_view_tweets_search(self):
        r = self.app.get(
            '/tweets?search=world',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 1

        assert tweets[0]['username'] == 'reneighbor'
        assert tweets[0]['body'] == 'hello world'
        assert tweets[0]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"


    def test_view_tweets_search_none_found(self):
        r = self.app.get(
            '/tweets?search=goodbye',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 0


    def test_view_tweets_verify_sort_order(self): 

        # altering the fixtures
        trenton_tweet = Tweet.query.filter_by(
            id = 2).first()

        trenton_tweet.date_created = datetime.date(2014, 1, 1)

        db.session.add(trenton_tweet)
        db.session.commit()


        r = self.app.get(
            '/tweets',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 2

        assert tweets[0]['username'] == 'reneighbor'
        assert tweets[0]['body'] == 'hello world'
        assert tweets[0]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"

        assert tweets[1]['username'] == 'trenton'
        assert tweets[1]['body'] == 'burning man'
        assert tweets[1]['date_created'] == "Wed, 01 Jan 2014 00:00:00 -0000"


    def test_view_tweets_not_following_anyone(self):
        r = self.app.get(
            '/tweets',
            headers=auth_headers('trenton'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 1

        assert tweets[0]['username'] == 'trenton'
        assert tweets[0]['body'] == 'burning man'
        assert tweets[0]['date_created'] == "Fri, 02 Jan 2015 00:00:00 -0000"

     


if __name__ == '__main__':
    unittest.main()


import unittest
import json
import datetime
from time import strftime

import sys
sys.path.append('/Users/renee/Projects/personal-projects/Pwitter')

from service import db
from service.models import Tweet
from base_test import BaseTest, auth_headers


class TweetResourceTest(BaseTest):

    def test_view_user_tweets(self):
        r = self.app.get(
            '/users/reneighbor/tweets',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 1

        assert tweets[0]['username'] == 'reneighbor'
        assert tweets[0]['body'] == 'hello world'
        assert tweets[0]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"


    def test_view_other_user_tweets(self):
        r = self.app.get(
            '/users/trenton/tweets',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 1
     
        assert tweets[0]['username'] == 'trenton'
        assert tweets[0]['body'] == 'burning man'
        assert tweets[0]['date_created'] == "Fri, 02 Jan 2015 00:00:00 -0000"


    def test_view_user_tweets_search(self):
        r = self.app.get(
            '/users/reneighbor/tweets?query=hello',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 1
     
        assert tweets[0]['username'] == 'reneighbor'
        assert tweets[0]['body'] == 'hello world'
        assert tweets[0]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"
        

    def test_view_user_tweets_search_none_found(self):
        r = self.app.get(
            '/users/reneighbor/tweets?search=goodbye',
            headers = auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 0


    def test_view_user_tweets_verify_sort_order(self):

        # altering the fixtures
        older_tweet = Tweet(
            username = 'reneighbor',
            user_id = 1,
            body = 'chicken dinner',
            date_created = datetime.date(2014, 1, 1)
        )

        db.session.add(older_tweet)
        db.session.commit()

        r = self.app.get(
            '/users/reneighbor/tweets',
            headers = auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        tweets = json.loads(r.data)['tweets']
        assert len(tweets) == 2

        assert tweets[0]['username'] == 'reneighbor'
        assert tweets[0]['body'] == 'hello world'
        assert tweets[0]['date_created'] == "Thu, 01 Jan 2015 00:00:00 -0000"

        assert tweets[1]['username'] == 'reneighbor'
        assert tweets[1]['body'] == 'chicken dinner'
        assert tweets[1]['date_created'] == "Wed, 01 Jan 2014 00:00:00 -0000"


    def test_view_user_tweets_no_user(self):
        r = self.app.get(
            '/users/nobody/tweets',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user nobody"


    def test_post_to_user_tweets_success(self):
        r = self.app.post(
            '/users/reneighbor/tweets',
            headers = auth_headers('reneighbor'),
            data = {'body' : 'foobar'}
        )

        assert r._status_code == 201
        
        tweet = json.loads(r.data)['tweet']

        assert tweet['username'] == 'reneighbor'
        assert tweet['body'] == 'foobar'
        assert tweet['date_created'] == strftime("%a, %d %b %Y %X -0000")
     

    def test_post_to_user_tweets_no_user(self):
        r = self.app.post(
            '/users/nobody/tweets',
            headers = auth_headers('reneighbor'),
            data = {'body' : 'foobar'}
        )

        assert r._status_code == 400
        
        response = json.loads(r.data)
        assert response['message'] == "No user nobody"
    

    def test_post_to_other_user_tweets_not_authorized(self):
        r = self.app.post(
            '/users/trenton/tweets',
            headers = auth_headers('reneighbor'),
            data = {'body' : 'foobar'}
        )

        assert r._status_code == 400
        
        response = json.loads(r.data)
        assert response['message'] == "Not authorized to tweet on behalf of another user"
     

    def test_post_to_user_tweets_body_missing(self):
        r = self.app.post(
            '/users/reneighbor/tweets',
            headers = auth_headers('reneighbor')
        )

        assert r._status_code == 400
        
        response = json.loads(r.data)
        assert response['message']['data']['message'] == "Missing required parameter body in the JSON body or the post body or the query string"
         

    def test_post_to_user_tweets_body_emtpy_string(self):
        r = self.app.post(
            '/users/reneighbor/tweets',
            headers = auth_headers('reneighbor'),
            data = {'body' : ''}
        )

        assert r._status_code == 400
        
        response = json.loads(r.data)
        assert response['message'] == "'body' argument is empty"
         
     

if __name__ == '__main__':
    unittest.main()
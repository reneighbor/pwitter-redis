import unittest
from base64 import b64encode
import datetime

from flask.ext.fixtures import Fixtures, loaders

from service import app, db
from service.models import Tweet



fixtures = Fixtures(app, db)

def auth_headers(user = 'reneighbor'):
    user_sid = ''
    auth_token = ''

    if user == 'reneighbor':
        user_sid = 'USf1ffeba94bf041'
        auth_token = '3c7dbf890b764f23'
    elif user == 'trenton':
        user_sid = 'US3d84e915339442'
        auth_token = 'e38140f35a5848f7'


    return  {
        'Authorization': 'Basic ' + 
        b64encode("{0}:{1}".format(user_sid, auth_token))
    }



class BaseTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object('testing.TestConfig')
        self.app = app.test_client()

        db.create_all()

        fixtures.load_fixtures(
            loaders.load('testing/fixtures/user.json'))
        fixtures.load_fixtures(
            loaders.load('testing/fixtures/broadcaster2_follower.json'))
        fixtures.load_fixtures(
            loaders.load('testing/fixtures/tweet.json'))


        # manually setting date_created; I don't believe 
        # Flask-Fixtures supports setting dates
        renee_tweet = Tweet.query.filter_by(id=1).first()
        renee_tweet.date_created = datetime.date(2015, 1, 1)

        trenton_tweet = Tweet.query.filter_by(id=2).first()
        trenton_tweet.date_created = datetime.date(2015, 1, 2)

        db.session.add(renee_tweet)
        db.session.add(trenton_tweet)
        db.session.commit()



    def tearDown(self): 
        db.session.remove()
        db.drop_all()




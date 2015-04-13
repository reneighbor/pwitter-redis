import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from flask.ext.httpauth import HTTPBasicAuth


logger = logging.getLogger('pwitter')
hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(filename)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

app = Flask(__name__)
app.config.from_object('config')




db = SQLAlchemy(app)
api = Api(app)
auth = HTTPBasicAuth()


# Importing resources after SqlAlchemy object is 
# created to avoid circular imports
from resources.users_resource import UsersList
from resources.users_broadcasters_resource import UsersBroadcastersList, UsersBroadcastersInstance
from resources.users_followers_resource import UsersFollowersList
from resources.tweets_resource import TweetsList
from resources.users_tweets_resource import UsersTweetsList




api.add_resource(TweetsList, 
    '/tweets')

api.add_resource(UsersTweetsList, 
    '/users/<string:username>/tweets')

api.add_resource(UsersFollowersList, 
    '/users/<string:username>/followers')

api.add_resource(UsersBroadcastersList, 
    '/users/<string:username>/broadcasters')

api.add_resource(UsersBroadcastersInstance, 
    '/users/<string:username>/broadcasters/<string:broadcaster_name>')



from datetime import datetime

from flask import g
from flask.ext.restful import fields, reqparse, marshal_with, marshal

from service import db
from service.models import Tweet, User
from base_resource import BaseResource


fields = {
    'username': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'body': fields.String,
}

class UsersTweetsList(BaseResource):

    def _get(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('search')
        args = parser.parse_args()



        user = User.query.filter_by(
            username = username).first()

        if not user:
            raise ValueError('No user {}'.format(username))



        query = Tweet.query.filter_by(user_id = user.id)

        if args.get('search'):
            query = query.filter(Tweet.body.like("%{}%".format(args['search'])))

        query = query.order_by(Tweet.date_created.desc())
        tweets = query.all()



        tweet_results = []

        for tweet in tweets:
            tweet_result = marshal({
                'username': tweet.username,
                'date_created': tweet.date_created,
                'body': tweet.body
            }, fields)

            tweet_results.append(tweet_result)

        return {'tweets': tweet_results}


    @marshal_with(fields, envelope='tweet')
    def _post(self, username):
        user = User.query.filter_by(
            username = username).first()

        if not user:
            raise ValueError("No user {}".format(username))

        if user.id != g.user.id:
            raise ValueError("Not authorized to tweet on behalf of another user")



        parser = reqparse.RequestParser()
        parser.add_argument('body',
            required=True)
        args = parser.parse_args()



        if args['body'] == '':
            raise ValueError("'body' argument is empty")

        tweet = Tweet(
            username = g.user.username,
            user_id = g.user.id,
            date_created = datetime.now(),
            date_updated = datetime.now(),
            body = args['body']
        )
        db.session.add(tweet)
        db.session.commit()



        result = {
            'username': tweet.username,
            'date_created': tweet.date_created,
            'body': tweet.body
        }

        return result, 201
        


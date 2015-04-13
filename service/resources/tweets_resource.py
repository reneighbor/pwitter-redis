from flask import g
from flask.ext.restful import fields, reqparse, marshal

from service.models import Broadcaster2Follower, Tweet
from base_resource import BaseResource


fields = {
    'username': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'body': fields.String,
}

class TweetsList(BaseResource):

    def _get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search')
        args = parser.parse_args()

        
        broadcasters = [g.user.id]

        broadcaster2followers = Broadcaster2Follower.query.filter_by(
            follower_id = g.user.id,
            active = True).all()

        for b2f in broadcaster2followers:
            broadcasters.append(b2f.broadcaster_id)



        query = Tweet.query.filter(Tweet.user_id.in_(broadcasters))

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
        
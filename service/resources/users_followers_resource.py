from flask.ext.restful import fields, marshal

from service.models import User, Broadcaster2Follower
from base_resource import BaseResource

fields = {
    'username': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_followed': fields.DateTime(dt_format='rfc822'),
}

class UsersFollowersList(BaseResource):

    def _get(self, username):
        user = User.query.filter_by(
            username=username).first()

        if not user:
            raise ValueError("No user {}".format(username))



        broadcaster2followers = Broadcaster2Follower.query.filter_by(
            broadcaster_id = user.id,
            active = True
        ).all()

        if len(broadcaster2followers) == 0:
            return {'followers': {}}



        follower_results = []

        for b2f in broadcaster2followers:
            follower = User.query.filter_by(
                id = b2f.follower_id
            ).first()

            if not follower:
                raise Exception("No user exists for follower with user_id {}".format(
                    b2f.follower_id))



            follower_result = marshal({
                    'username': follower.username,
                    'date_created': follower.date_created,
                    'date_followed': b2f.date_created,
                }, fields)

            follower_results.append(follower_result)


        return {'followers': follower_results}
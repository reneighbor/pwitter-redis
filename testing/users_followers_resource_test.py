import unittest
import json

import sys
# needed to import service
sys.path.append('/Users/renee/Projects/personal-projects/Pwitter')
from service import db
from service.models import User
from base_test import BaseTest, auth_headers

class UsersFollowersResourceTest(BaseTest):

    def test_view_user_followers(self):
        r = self.app.get(
            '/users/trenton/followers',
            headers=auth_headers('trenton'),
        )

        assert r._status_code == 200

        broadcasters = json.loads(r.data)['followers']
        assert len(broadcasters) == 1

        assert broadcasters[0]['username'] == 'reneighbor'
        assert broadcasters[0]['date_created'] == None
        assert broadcasters[0]['date_followed'] == None


    def test_view__other_user_followers(self):
        r = self.app.get(
            '/users/trenton/followers',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        broadcasters = json.loads(r.data)['followers']
        assert len(broadcasters) == 1

        assert broadcasters[0]['username'] == 'reneighbor'
        assert broadcasters[0]['date_created'] == None
        assert broadcasters[0]['date_followed'] == None


    def test_view_user_followers_no_user(self):
        r = self.app.get(
            '/users/nobody/followers',
            headers=auth_headers('reneighbor'),
        )
        
        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == 'No user nobody'


    def test_view_user_followers_no_followers(self):
        r = self.app.get(
            '/users/reneighbor/followers',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        followers = json.loads(r.data)['followers']
        assert len(followers) == 0


    def test_view_user_followers_no_user_for_follower(self):

        # altering the fixtures
        reneighbor = User.query.filter_by(
            id = 1).first()

        db.session.delete(reneighbor)
        db.session.commit()


        r = self.app.get(
            '/users/trenton/followers',
            headers=auth_headers('trenton'),
        )

        assert r._status_code == 500

        response = json.loads(r.data)
        assert response['message'] == 'No user exists for follower with user_id 1'





if __name__ == '__main__':
    unittest.main()

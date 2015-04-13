import unittest
import json
from time import strftime

import sys
# needed to import service
sys.path.append('/Users/renee/Projects/personal-projects/Pwitter')
from service import db
from service.models import User
from base_test import BaseTest, auth_headers


class UsersBroadcastersResourceTest(BaseTest):

    def test_view_user_broadcasters(self):
        r = self.app.get(
            '/users/reneighbor/broadcasters',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 200

        broadcasters = json.loads(r.data)['broadcasters']
        assert len(broadcasters) == 1

        assert broadcasters[0]['username'] == 'trenton'
        assert broadcasters[0]['date_created'] == None
        assert broadcasters[0]['date_followed'] == None


    def test_view_other_user_broadcasters(self):
        r = self.app.get(
            '/users/reneighbor/broadcasters',
            headers=auth_headers('trenton'),
        )

        assert r._status_code == 200

        broadcasters = json.loads(r.data)['broadcasters']
        assert len(broadcasters) == 1

        assert broadcasters[0]['username'] == 'trenton'
        assert broadcasters[0]['date_created'] == None
        assert broadcasters[0]['date_followed'] == None


    def test_view_user_no_user(self):
        r = self.app.get(
            '/users/nobody/broadcasters',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user nobody"


    def test_view_user_not_following_anyone(self):
        r = self.app.get(
            '/users/trenton/broadcasters',
            headers=auth_headers('trenton'),
        )

        assert r._status_code == 200

        broadcasters = json.loads(r.data)['broadcasters']
        assert len(broadcasters) == 0


    def test_view_user_broadcaster_no_user_for_broadcaster(self):
        
        # altering the fixtures
        trenton = User.query.filter_by(
            id = 2).first()

        db.session.delete(trenton)
        db.session.commit()

        r = self.app.get(
            '/users/reneighbor/broadcasters',
            headers=auth_headers('reneighbor'),
        )

        assert r._status_code == 500

        response = json.loads(r.data)
        assert response['message'] == 'No user exists for broadcaster with ID: 2'


    def test_post_user_broadcaster_success(self):
        r = self.app.post(
            '/users/trenton/broadcasters',
            headers=auth_headers('trenton'),
            data={'username':'reneighbor'}
        )

        assert r._status_code == 201

        broadcaster = json.loads(r.data)['broadcaster']

        assert broadcaster['username'] == 'reneighbor'
        assert broadcaster['date_created'] == None
        assert broadcaster['date_followed'] == strftime("%a, %d %b %Y %X -0000")


    def test_post_user_broadcaster_no_user(self):
        r = self.app.post(
            '/users/nobody/broadcasters',
            headers=auth_headers('trenton'),
            data={'username':'reneighbor'}
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user nobody"


    def test_post_to_other_user_broadcaster_not_authorized(self):
        r = self.app.post(
            '/users/reneighbor/broadcasters',
            headers=auth_headers('trenton')
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "Not authorized to follow users on behalf another account"


    def test_post_to_user_broadcaster_username_missing(self):
        r = self.app.post(
            '/users/trenton/broadcasters',
            headers=auth_headers('trenton')
        )

        assert r._status_code == 400

        response = json.loads(r.data)   
        assert response['message']['data']['message'] == "Missing required parameter username in the JSON body or the post body or the query string"


    def test_post_to_user_broadcaster_userame_empty_string(self):
        r = self.app.post(
            '/users/trenton/broadcasters',
            headers=auth_headers('trenton'),
            data={'username':''}
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "'username' argument is empty"


    def test_post_to_user_broadcaster_no_broadcaster_found(self):
        r = self.app.post(
            '/users/trenton/broadcasters',
            headers=auth_headers('trenton'),
            data={'username':'noah'}
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user found for 'noah'"


    def test_post_to_user_broadcaster_already_following_broadcaster(self):
        r = self.app.post(
            '/users/reneighbor/broadcasters',
            headers=auth_headers('reneighbor'),
            data={'username':'trenton'}
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "Already following user 'trenton'"



    def test_delete_user_broascaster_success(self):
        r = self.app.delete(
            'users/reneighbor/broadcasters/trenton',
            headers = auth_headers('reneighbor')
        )

        assert r._status_code == 204

        r = self.app.get(
            'users/reneighbor/broadcasters',
            headers = auth_headers('reneighbor')
        )

        broadcasters = json.loads(r.data)['broadcasters']
        assert len(broadcasters) == 0


    def test_delete_user_broascaster_success(self):
        r = self.app.delete(
            'users/reneighbor/broadcasters/trenton',
            headers = auth_headers('reneighbor')
        )

        assert r._status_code == 204

        r = self.app.get(
            'users/reneighbor/broadcasters',
            headers = auth_headers('reneighbor')
        )

        broadcasters = json.loads(r.data)['broadcasters']
        assert len(broadcasters) == 0


    def test_delete_user_broascaster_no_user(self):
        r = self.app.delete(
            'users/nobody/broadcasters/trenton',
            headers = auth_headers('reneighbor')
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user nobody"


    def test_delete_user_broascaster_not_authorized_on_behalf(self):
        r = self.app.delete(
            'users/reneighbor/broadcasters/trenton',
            headers = auth_headers('trenton')
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "Not authorized to unfollow users on behalf another account"
        

    def test_delete_user_broadcaster_no_user_for_broadcaster_name(self):
        r = self.app.delete(
            'users/reneighbor/broadcasters/nobody',
            headers = auth_headers('reneighbor')
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "No user found for 'nobody'"
        

    def test_delete_user_broascaster_not_currently_following(self):
        r = self.app.delete(
            'users/trenton/broadcasters/reneighbor',
            headers = auth_headers('trenton')
        )

        assert r._status_code == 400

        response = json.loads(r.data)
        assert response['message'] == "Not currently following reneighbor"
      


if __name__ == '__main__':
    unittest.main()

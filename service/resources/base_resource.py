from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash

from flask import g
from flask.ext.restful import Resource

from service import auth, logger
from service.models import User


@auth.verify_password
def verify_pw(user_sid, password):
	try:
		user = User.query.filter_by(user_sid=user_sid).first()
		
		if not user:
			raise Exception("No user for {}".format(user_sid))

		if check_password_hash(user.hashed_token, password):
			g.user = user
			return True

	except Exception as e:
		logger.error("Error: %s" % e)


class BaseResource(Resource):
	method_decorators = [auth.login_required] 

	def check_method(self, method):
		if method not in dir(self):
			raise NotImplementedError
		return


	def get(self, *args, **kwargs):
		try:
			self.check_method("_get")
			data = self._get(*args, **kwargs)
			return data
		except NotImplementedError:
			error = {'message': "Method not allowed"}
			return error, 405
		except ValueError as e:
			error = {'message': e.message}
			return error, 400
		except BaseException as e:
			error = {'message': e.message}
		return error, 500


	def post(self, *args, **kwargs):
		try:
			self.check_method("_post")	
			data = self._post(*args, **kwargs)
			return data
		except NotImplementedError:
			error = {'message': "Method not allowed"}
			return error, 405
		except HTTPException as e:
			error = {'message': vars(e)}
			return error, 400	
		except ValueError as e:
			error = {'message': e.message}
			return error, 400
		except BaseException as e:
			error = {'message': e.message}
		return error, 500


	def delete(self, *args, **kwargs):
		try:
			self.check_method("_delete")
			data = self._delete(*args, **kwargs)
			return data
		except NotImplementedError:
			error = {'message': "Method not allowed"}
			return error, 405
		except ValueError as e:
			error = {'message': e.message}
			return error, 400
		except Exception as e:
			error = {'message': e.message}
		return error, 500




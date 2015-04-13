import sys
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from service import db
from service.models import User




def random_string(string_length=14):

    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.replace("-","") # Remove the UUID '-'.
    
    return random[0:string_length] # Return the random string.



if len(sys.argv) <= 1:
	print "Username is required"
	sys.exit()

username = sys.argv[1]

existing_users = User.query.filter_by(
	username=username)

if existing_users.count() > 0:
	print "User with name {} already exists".format(username)
	sys.exit()


sid = 'US' + random_string(14)
auth_token = random_string(16)
hashed_token = generate_password_hash(auth_token)

user = User(username = username,
			user_sid = sid,
			hashed_token = hashed_token,
			date_created = datetime.now(),
			date_updated = datetime.now())

# creating DB session via Flask
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


db.session.add(user)
db.session.commit()

db.session.close()

print "Created user {}, user_sid: {}, auth_token : {}".format(username, sid, auth_token) 



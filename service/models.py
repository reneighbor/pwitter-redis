import datetime
from service import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    username = db.Column(db.String(64), unique=True)
    user_sid = db.Column(db.String(16), unique=True)
    hashed_token = db.Column(db.String(16), unique=True)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Broadcaster2Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    broadcaster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Broadcaster2Follower %r, %r>' % (self.broadcaster_id, self.follower_id)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    body = db.Column(db.String(140))

    def __repr__(self):
        return '<Tweet %r>' % (self.body)


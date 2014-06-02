from chutiyapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from wtforms import Form, TextField, FloatField, validators


db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(10000))
    username = db.Column(db.String(50))
    locx = db.Column(db.Float)
    locy = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    edited_at = db.Column(db.DateTime)

    def __init__(self, title, body, username, 
        locx, locy, created_at=None, edited_at=None):
        self.title = title
        self.body = body
        self.username = username
        self.locx = locx
        self.locy = locy
        if created_at is None:
            created_at = datetime.utcnow()
        self.created_at = created_at
        if edited_at is None:
            edited_at = datetime.utcnow()
        self.edited_at = edited_at

    def __repr__(self):
        return '<Post: %s>' % self.title

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            body = self.body,
            username = self.username,
            locx = self.locx,
            locy = self.locy,
            created_at = str(datetime.utcnow() - self.created_at),
            edited_at = str(datetime.utcnow() - self.edited_at),
            )

class PostForm(Form):
    title = TextField('Title', [validators.length(min=3, max=140)])
    body = TextField('Text', [validators.length(max=5000)])
    locx = FloatField('Longitude', [validators.NumberRange(min=-180, max=180)])
    locy = FloatField('latitude', [validators.NumberRange(min=-90, max=90)])
    

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(5000))
    username = db.Column(db.String(50))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post',
        backref=db.backref('replies', lazy='dynamic'))

    def __init__(self, post, body, username):
        self.post = post
        self.body = body
        self.username = username

    def __repr__(self):
        return '<Reply: %s>' % self.body[:100]

    def to_dict(self):
        return dict(
            post_id = self.post_id,
            post = self.post.__repr__(),
            body = self.body,
            username = self.username)



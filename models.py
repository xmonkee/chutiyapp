from chutiyapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from wtforms import Form, TextField, FloatField, validators
from hashlib import md5
from geoloc import geoloc


db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    slug = db.Column(db.String(10),unique=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(10000))
    username = db.Column(db.String(50))
    locx = db.Column(db.Float)
    locy = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    edited_at = db.Column(db.DateTime)
    number_replies = db.Column(db.Integer)
    sticky = db.Column(db.Boolean)

    def __init__(self, title, body, username, 
        locx, locy, created_at=None, edited_at=None):
        self.slug = md5(str(datetime.utcnow())).hexdigest()[:10]
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
        self.number_replies = 0
        self.sticky = False

    def __repr__(self):
        return '<Post: %s>' % self.title

    def to_dict(self):
        return dict(
            id = self.id,
            slug = self.slug,
            title = self.title,
            body = self.body,
            username = self.username,
            locx = self.locx,
            locy = self.locy,
            created_at = str(datetime.utcnow() - self.created_at),
            edited_at = str(datetime.utcnow() - self.edited_at),
            )
    
    ###################################################################
    # Generates posts for the front page. We filter by location here, #
    # we sort it by editing time and we cut off our results at the    #
    # ITEMS_PER_PAGE number                                           #
    ###################################################################
    @staticmethod
    def get_all(loc):
        bounds = geoloc.bounds(loc)
        stickied = Post.query.filter(Post.sticky).all()
        local = Post.query.filter(Post.locy > bounds['lower']['lat'],
                                 Post.locy < bounds['upper']['lat'],
                                 Post.locx > bounds['lower']['lon'],
                                 Post.locy < bounds['upper']['lon'],
                                ).order_by(Post.edited_at.desc())[:app.config['POSTS_PER_PAGE']]
        return stickied+local

    def get_replies(self):
        return self.replies.order_by(Reply.created_at.desc())[:app.config['REPLIES_PER_PAGE']]

    @staticmethod
    def get_post_from_slug(slug):
        return Post.query.filter_by(slug = slug).first()

class PostForm(Form):
    title = TextField('Title', [validators.length(min=3, max=140)])
    body = TextField('Text', [validators.length(max=5000)])

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(5000))
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post',
        backref=db.backref('replies', lazy='dynamic'))

    def __init__(self, post, body, username, created_at=None):
        self.post = post
        self.body = body
        self.username = username
        if created_at is None:
            created_at = datetime.utcnow()
        self.created_at = created_at
        self.post.edited_at = created_at
        self.post.number_replies = self.post.number_replies + 1


    def __repr__(self):
        return '<Reply: %s>' % self.body[:100]

    def to_dict(self):
        return dict(
            post_id = self.post_id,
            post = self.post.__repr__(),
            body = self.body,
            username = self.username)

class LoginForm(Form):
    lon = FloatField('Longitude', [validators.required(), validators.NumberRange(min=-180, max=180)])
    lat = FloatField('latitude', [validators.required(), validators.NumberRange(min=-90, max=90)])

class ReplyForm(Form):
    body = TextField('Reply', [validators.length(min=1, max=5000)])
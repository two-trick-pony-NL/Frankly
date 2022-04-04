from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#This file manages the columns defined in the database

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    phonenumber = db.Column(db.String(20))
    isadmin = db.Column(db.Boolean())
    haspaid = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True) #This is all posts for this user
    campaigns = db.relationship('Campaign', backref='user', passive_deletes=True) #This is all campaigns for this user
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    customquestion0 = db.Column(db.String(150))
    customquestion1 = db.Column(db.String(150))
    customquestion2 = db.Column(db.String(150))
    customquestion3 = db.Column(db.String(150))


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaignname = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    customquestion1 = db.Column(db.String(150))
    customquestion1 = db.Column(db.String(150))
    customquestion2 = db.Column(db.String(150))
    customquestion3 = db.Column(db.String(150))
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    rating = db.Column(db.Integer, nullable=True)
    email = db.Column(db.Text, nullable=True)
    allow_contact = db.Column(db.Boolean, nullable=True)
    campaign = db.Column(db.Integer, db.ForeignKey(
        'campaign.id', ondelete="CASCADE"), nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

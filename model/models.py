from flask_sqlalchemy import SQLAlchemy
from lib.tools import *
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def checkpw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __repr__(self):
        return '<username %r>' % self.username

class VideoYT(db.Model):
    __tablename__ = "video_yt"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    link = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False)
    
    def __init__(self, title, channel, views, date, link, thumbnail):
        self.title = title
        self.channel = channel
        self.views = views
        self.date = date
        self.link = link
        self.thumbnail = thumbnail
    
    def getViews(self):
        return format_views(self.views)
    
    def getStatus(self):
        # f = '%Y-%m-%d %H:%M:%S'
        return time_status(self.date)
    
    def __repr__(self):
        return '<title %r>' % self.title

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www.gannett-cdn.com/presto/2020/03/17/USAT/c0eff9ec-e0e4-42db-b308-f748933229ee-XXX_ThinkstockPhotos-200460053-001.jpg"
def connect_db(app):
    """Models for Blogly."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""  #more description on the model itself, clarify possible confusion

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    first_name = db.Column(db.String(50), 
                            nullable=False)

    last_name = db.Column(db.String(50),     # could also use db.text
                            nullable=False)
    
    image_url = db.Column(db.String, 
                default=DEFAULT_IMG_URL,
                nullable=False) #originally was nullable - if not given, it's not an unknown

    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(
        db.DateTime, 
        nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, 
              db.ForeignKey("users.id"), 
              nullable=False) #always remember!

    tags = db.relationship('Tag',
                            secondary='posts_tags',
                            backref='posts')


class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(
                db.Integer, 
                primary_key=True, 
                autoincrement=True)
    name = db.Column( 
                db.String(20),
                nullable=False)

class PostTag(db.Model):
    """PostTag"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
            db.ForeignKey("posts.id"), 
            nullable=False,
            primary_key=True) 
    
    tag_id = db.Column(db.Integer, 
            db.ForeignKey("tags.id"), 
            nullable=False,
            primary_key=True)
         



from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://i.pinimg.com/originals/7f/26/e7/7f26e71b2c84e6b16d4f6d3fd8a58bca.png'
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
    
    image_url = db.Column(db.String, default=DEFAULT_IMG_URL)

    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """User"""  #more description on the model itself, clarify possible confusion

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.utcnow)

    user_id = db.Column(db.Integer, 
              db.ForeignKey("users.id"), 
              nullable=False)

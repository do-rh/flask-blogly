
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Models for Blogly."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    default_image_url = 'https://i.pinimg.com/originals/7f/26/e7/7f26e71b2c84e6b16d4f6d3fd8a58bca.png'

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    first_name = db.Column(db.String(50), 
                            nullable=False)

    last_name = db.Column(db.String(50), 
                            nullable=False)
    
    image_url = db.Column(db.String, default=default_image_url)


"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'this-is-my-top-level-secret'
debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# db.create_all()

@app.get('/')
def home_page():
    return redirect('/users')

@app.get('/users')
def show_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)



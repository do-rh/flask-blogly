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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.create_all()

@app.get('/')
def home_page():
    """Redirect to /users"""
    return redirect('/users')

@app.get('/users')
def show_all_users():
    """Show all users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """Show new user form"""

    return render_template('user_form.html')

@app.post('/users/new')
def add_user():
    """Getting form inputs and adding it to the User database, 
    redirect to /users when complete."""

    first = request.form['first-name']
    last = request.form['last-name']
    image_url = request.form['image-url']

    new_user = User(first_name=first, last_name=last, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """Showing individual user info."""

    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)

@app.get('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show edit user page/form"""
    
    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html',user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    """handling user info update, update database and redirect to users page"""
    user = User.query.get_or_404(user_id)

    first = request.form['first-name']
    last = request.form['last-name']
    image_url = request.form['image-url']
    
    user.first_name = first
    user.last_name = last
    user.image_url = image_url

    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """delete user from database, redirect to /users after deletion"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
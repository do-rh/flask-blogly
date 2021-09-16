"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post

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
    posts = user.posts
    return render_template('user_info.html', user=user, posts=posts)

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

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """show new post HTML"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """add new post to database and redirect to user's page"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """render post.html, show details of the post"""
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post.html',user=user, post=post)

@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """render post edit form"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html',post=post)

@app.post('/posts/<int:post_id>/edit')
def update_post_info(post_id):
    """update post info in database and redirect to post page"""
    post = Post.query.get_or_404(post_id)
    title = request.form["title"]
    content = request.form["content"]
    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """delete the post in database and redirect to user info page"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()


# Add pets
whiskey = User(first_name='Whiskey', last_name="dog")
bowser = User(first_name='Bowser', last_name="dog")
spike = User(first_name='Spike', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.commit()
whiskey_id = whiskey.id
bowser_id = bowser.id
spike_id = spike.id

new_post = Post(title="Woof Woof", content="I love whiskey!", user_id=whiskey_id)
new_post2 = Post(title="Woof Woof meow", content="I love whiskey meow!", user_id=bowser_id)
db.session.add(new_post)
db.session.add(new_post2)
db.session.commit()
post_id1 = new_post.id
post_id2= new_post2.id


tag1= Tag(name='fun')
tag2=Tag(name='Thriller')
db.session.add(tag1)
db.session.add(tag2)
db.session.commit()
tag1_id = tag1.id
tag2_id = tag2.id

post_tag = PostTag(post_id=post_id1, tag_id=tag2_id)
post_tag2 = PostTag(post_id=post_id2, tag_id=tag2_id)
db.session.add(post_tag)
db.session.add(post_tag2)
# Commit--otherwise, this never gets saved!
db.session.commit()
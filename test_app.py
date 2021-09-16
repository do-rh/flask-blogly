from unittest import TestCase
from app import app
from models import DEFAULT_IMG_URL, db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):

    def setUp(self):
        """Add sample user and sample post"""
        Post.query.delete()
        User.query.delete()
        
        new_user = User(first_name="Taco-Test",
                        last_name="Cat",
                        image_url=DEFAULT_IMG_URL)
        
        db.session.add(new_user)
        db.session.commit()

        self.user_id = new_user.id
        self.first_name = new_user.first_name
        self.last_name = new_user.last_name

        new_post = Post(title="Burrito-Test",
                        content="Porcupines love burritos more than tacos!",
                        user_id=self.user_id)
        
        db.session.add(new_post)
        db.session.commit()

        self.post_id = new_post.id
        self.title = new_post.title
        self.content = new_post.content

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback() #if an error happened in any test before committing, then rollback any random changes
    
    def test_show_all_users(self):
        """test if route renders page that show all users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html)     #check for specific user on list

    def test_add_user(self):
        """test adding new user with test user info"""

        with app.test_client() as client:
            resp = client.post("/users/new",
                            data={
                                "first-name": "TEST-DOG-DOG",
                                "last-name": "CAT-CAT",
                                "image-url": DEFAULT_IMG_URL}, 
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 
            self.assertIn("TEST-DOG-DOG", html)
            self.assertIn("CAT-CAT", html)  
    
    def test_show_user_info(self):
        """test show user info page of test user"""

        with app.test_client() as client:
            user_id = self.user_id
            resp = client.get(f"/users/{user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn("Taco-Test", html)
            self.assertIn("Edit</a>", html) 
            self.assertIn("Delete</button>", html)

    def test_show_new_user_form(self):
        """test showing add new user form"""

        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertIn("<h1>Create a User</h1>", html)
            self.assertIn("Add</button>", html) 
    
    def test_delete_user(self):
        """test user deletion -- delete the test user"""

        with app.test_client() as client:
            user_id = self.user_id
            resp = client.post(f"/users/{user_id}/delete",
                              follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertNotIn("Taco-Test", html)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 

    def test_show_new_post_form(self):
        """testing route for showing the new post form"""

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertIn(f'Add a post for {self.first_name} {self.last_name}', html)
            self.assertIn("Add</button>", html) 

    def test_add_new_post(self):
        """testing the post request for adding a new post"""

        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', 
                               data={
                                   'title': 'test-title', 
                                   'content': 'blahblahblahmeowmeowmeow'
                                   },
                                   follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("test-title", html)
            self.assertIn("Edit</a>", html) 
            self.assertIn("Delete</button>", html)

    def test_show_post(self):
        """test for showing the post details"""

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertIn(self.title, html)
            self.assertIn(self.content, html)
            self.assertIn(f'{self.first_name} {self.last_name}', html)

    def test_update_post_info(self):
        """test for editing a post"""

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', 
                               data={"title": "Mushu", 
                               "content": "jk, i don't like burritos, i like Mushu!"}, 
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Mushu", html)
            self.assertIn("like burritos, i like Mushu!", html)
            self.assertIn(f'{self.first_name} {self.last_name}', html)

    def test_delete_post(self):
        """test for deleting a post"""

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete',
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn(f'{self.first_name} {self.last_name}', html)
            self.assertNotIn(self.title, html)
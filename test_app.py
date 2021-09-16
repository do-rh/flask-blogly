from unittest import TestCase
from app import app
from models import db, User

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
        """Add sample user"""
        User.query.delete()
        new_user = User(first_name="Taco-Test",
                        last_name="Cat",
                        image_url="https://images-na.ssl-images-amazon.com/images/I/41nJXMOVSlL._SX331_BO1,204,203,200_.jpg")
        db.session.add(new_user)
        db.session.commit()
        self.user_id = new_user.id

        # new_user2 = User(first_name="Taco-Test2",
        #                 last_name="Cat",
        #                 image_url="https://images-na.ssl-images-amazon.com/images/I/41nJXMOVSlL._SX331_BO1,204,203,200_.jpg")
        # db.session.add(new_user2)
        # db.session.commit()
        # self.user_id2 = new_user2.id
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_show_all_users(self):
        """test if route renders page that show all users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html)     

    def test_add_user(self):
        # """ test adding new user with test user info"""      # REFACTOR TEST DATA, SAVE IN VARIABLE
        with app.test_client() as client:
            resp = client.post("/users/new",
                            data={
                                "first-name": "TEST-DOG-DOG",
                                "last-name": "CAT-CAT",
                                "image-url": "https://images-na.ssl-images-amazon.com/images/I/41nJXMOVSlL._SX331_BO1,204,203,200_.jpg"}, 
                                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 
            self.assertIn("TEST-DOG-DOG", html)
            self.assertIn("CAT-CAT", html)  
    

    def test_show_user_info(self):
        """test user info page of test user"""
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
            resp = client.post(f"/users/{user_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Taco-Test", html)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 


    

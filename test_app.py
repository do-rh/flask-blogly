from unittest import TestCase
from app import app
from models import db, connect_db, User
connect_db(app)

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True


class BloglyTestCase(TestCase):
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
                                "first-name": "Taco-Test",
                                "last-name": "Cat",
                                "image-url": "https://images-na.ssl-images-amazon.com/images/I/41nJXMOVSlL._SX331_BO1,204,203,200_.jpg"}, 
                                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 
            self.assertIn("Taco-Test", html)
            self.assertIn("Cat", html)  
    
    def get_test_user_id(self):
        """get the user_id for the test user, and return id"""
        user = User.query.filter(User.first_name=="Taco-Test", 
                                User.last_name=="Cat", 
                                User.image_url=="https://images-na.ssl-images-amazon.com/images/I/41nJXMOVSlL._SX331_BO1,204,203,200_.jpg")
        user_id = user.one().id
        return user_id

    def test_show_user_info(self):
        """test user info page of test user"""
        with app.test_client() as client:
            user_id = BloglyTestCase.get_test_user_id(self)
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
    

class BloglyDeleteCase(TestCase):
    def test_delete_user(self):
        """test user deletion -- delete the test user"""
        with app.test_client() as client:
            user_id = BloglyTestCase.get_test_user_id(self)
            resp = client.post(f"/users/{user_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Taco-Test", html)
            self.assertIn("<h1> Users </h1>", html)
            self.assertIn("<ul>", html) 


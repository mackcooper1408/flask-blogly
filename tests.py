from unittest import TestCase
from app import app, User


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BloglyTest(TestCase):
    

    def setUp(self):
        """Before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_homepage(self):
        """Tests base template and users template renders after reroute"""

        with self.client as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="text-center">Users</h1>', html)
            self.assertIn('<header>', html)
            
    def test_show_new_users(self):
        """New user form displayed"""

        with self.client as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="text-center">Create a user</h1>', html)
            self.assertIn('<header>', html)

    def test_create_new_user(self):
        """Test that creating user adds user to DB and reroutes to users"""

        with self.client as client:
            response = client.post('/users/new',
                                   data={"first-name": "AAA", "last-name": "BBB", "image-url": "http://www.image.com"},
                                   follow_redirects=True)
            user1 = User.query.filter(User.first_name == "AAA").first()

            html = response.get_data(as_text=True)

            """ Testing Routing """
            self.assertEqual(response.status_code, 200)

            """ Testing User Display """
            self.assertIn('<h1 class="text-center">Users</h1>', html)
            self.assertEqual(user1.first_name, "AAA")
            
    def test_show_user_detail(self):
        """Tests base template and users template renders after reroute"""

        with self.client as client:

            user1 = User.query.get_or_404(1)

            response = client.get(f'/users/{user1.id}', follow_redirects=True)

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>{user1.full_name}</h1>', html)

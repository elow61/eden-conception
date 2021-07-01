""" All tests for the user views application """
from django.test import TestCase, override_settings
from django.db.models.query import QuerySet
from user.models import User


class RegisterViewTest(TestCase):
    """ Class to test the view register account """

    def setUp(self):
        self.form_class = {
            'username': 'test_form',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'email@test.com',
            'password1': 'test_password_1',
            'password2': 'test_password_1',
        }

    def test_get_request(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        response = self.client.post('/register/', self.form_class)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_post_request_if_wrong_form(self):
        form = self.form_class
        form['password2'] = 'wrong_password'
        response = self.client.post('/register/', form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, '/register/')

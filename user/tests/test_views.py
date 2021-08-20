""" All tests for the user views application """
from django.test import TestCase, override_settings
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from django.core import mail
from user.models import User


class RegisterViewTest(TestCase):
    """ Class to test the view register account """

    def setUp(self):
        self.form_class = {
            'username': 'test_form',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'email@test.com',
            'image': self.get_image_file(),
            'password1': 'test_password_1',
            'password2': 'test_password_1',
        }

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_get_request(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        response = self.client.post(reverse('user:register'), self.form_class)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('project:dashboard'))

    def test_post_request_if_wrong_form(self):
        form = self.form_class
        form['password2'] = 'wrong_password'
        response = self.client.post(reverse('user:register'), form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, reverse('user:register'))


class PasswordResetView(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='test_username',
            first_name='test_first_name',
            last_name='test_last_name',
            email='email@test.com',
            password='test_password_61',
        )
        self.form = {'email': 'email@test.com'}

    def test_reset_password(self):
        response = self.client.get('/reset_password/')
        self.assertEqual(response.status_code, 200)

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_send_email(self):
        response = self.client.post('/reset_password/', self.form)
        self.assertEqual(response.url, '/reset_password_sent/')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')

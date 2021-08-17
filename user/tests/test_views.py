""" All tests for the user views application """
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.core.files.base import File


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

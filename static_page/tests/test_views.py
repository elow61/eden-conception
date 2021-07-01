""" Units tests for the home app """
from django.test import TestCase


class IndexViewTest(TestCase):

    def test_get_request(self):
        response = self.client.get('/')
        self.assertTemplateUsed('static_page/index.html')
        self.assertEqual(response.status_code, 200)


class LegalNoticeViewTest(TestCase):

    def test_get_request(self):
        response = self.client.get('/legal-notices/')
        self.assertTemplateUsed('static_page/legal_notice.html')
        self.assertEqual(response.status_code, 200)

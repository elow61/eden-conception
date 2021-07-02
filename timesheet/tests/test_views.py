from django.test import TestCase
from http import HTTPStatus
from user.models import User


class TimesheetViewTest(TestCase):

    fixtures = ['timesheet.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_username_2',
            first_name='test_first_name',
            last_name='test_last_name',
            email='email@tests.com',
            password='test_password_61',
        )

    def test_receipt_form_fields(self):
        datas = {
            'assigned_to': self.user.id,
            'deadline': '12/06/2021',
            'task_id': 1,
            'planned_hours': '02:00',
            'name': 'name',
            'created_at': '2021-06-29 00:00:00+02',
            'user': self.user.id,
            'description': 'a little description.',
            'unit_hour': 2,
        }

        self.client.login(username='email@tests.com', password='test_password_61')
        response = self.client.post('/update_task/', datas)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.logout()

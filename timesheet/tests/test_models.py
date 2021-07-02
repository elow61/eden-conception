""" All tests for the product models application """
from django.test import TestCase
from timesheet.models.timesheet import Timesheet
from project.models.task import Task
from user.models import User


class TimesheetModelTest(TestCase):

    fixtures = ['timesheet.json']

    def test_user_relation(self):
        timesheet = Timesheet.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEqual(user.first_name, timesheet.user.first_name)

    def test_description_max_length(self):
        timesheet = Timesheet.objects.get(pk=1)
        max_length = timesheet._meta.get_field('description').max_length
        self.assertEqual(max_length, 200)

    def test_unit_hour_default(self):
        timesheet = Timesheet.objects.get(pk=1)
        default = timesheet._meta.get_field('unit_hour').default
        self.assertEqual(default, 0)

    def test_task_relation(self):
        timesheet = Timesheet.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        self.assertEqual(task.index, timesheet.task.index)

    def test_unit_hour_time(self):
        timesheet = Timesheet.objects.get(pk=1).unit_hour_time
        self.assertEqual(timesheet, '02:00')

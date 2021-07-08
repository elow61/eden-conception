""" All tests for the product models application """
from django.test import TestCase
from project.models.project import Project
from project.models.list import List
from project.models.task import Task
from user.models import User


class ProjectModelTest(TestCase):

    fixtures = ['datas.json']

    def test_user_relation(self):
        project = Project.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEqual(user.first_name, project.user.first_name)

    def test_name_max_length(self):
        project = Project.objects.get(pk=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_number_task_default(self):
        project = Project.objects.get(pk=1)
        default = project._meta.get_field('number_task').default
        self.assertEqual(default, 0)


class ListModelTest(TestCase):

    fixtures = ['datas.json']

    def test_name_max_length(self):
        p_list = List.objects.get(pk=1)
        max_length = p_list._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_project_relation(self):
        p_list = List.objects.get(pk=1)
        project = Project.objects.get(pk=1)
        self.assertEqual(project.name, p_list.project.name)


class TaskModelTest(TestCase):

    fixtures = ['datas.json']

    def test_name_max_length(self):
        task = Task.objects.get(pk=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_list_relation(self):
        task = Task.objects.get(pk=1)
        p_list = List.objects.get(pk=1)
        self.assertEqual(p_list.name, task.project_list.name)

    def test_planned_hours_default(self):
        task = Task.objects.get(pk=1)
        default = task._meta.get_field('planned_hours').default
        self.assertEqual(default, 0)

    def test_effective_hours_default(self):
        task = Task.objects.get(pk=1)
        default = task._meta.get_field('effective_hours').default
        self.assertEqual(default, 0)

    def test_remaining_hours_default(self):
        task = Task.objects.get(pk=1)
        default = task._meta.get_field('remaining_hours').default
        self.assertEqual(default, 0)

    def test_planned_hours_time(self):
        task = Task.objects.get(pk=1).planned_hours_time
        self.assertEqual(task, '03:30')

    def test_effective_hours_time(self):
        task = Task.objects.get(pk=1).effective_hours_time
        self.assertEqual(task, '02:00')

    def test_remaining_hours_time(self):
        task = Task.objects.get(pk=1).remaining_hours_time
        self.assertEqual(task, '01:30')

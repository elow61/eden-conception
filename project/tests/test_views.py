from django.test import TestCase

from user.models import User
from project.models.project import Project
from project.models.task import Task


class TaskView(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()

    def test_get_request_user_authenticate(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(f'/project-{project.id}/task-{task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/tasks/tasks.html')
        self.client.logout()

    def test_get_request_user_no_authenticate(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        response = self.client.get(f'/project-{project.id}/task-{task.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/project-{project.id}/task-{task.id}/')

    def test_post_request_user_authenticate(self):
        task = Task.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(f'/{task.id}/update/', task_id=task.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], task)
        self.assertEqual(type(response.context['task']), Task)
        self.assertTemplateUsed(response, 'project/tasks/forms/update_task.html')
        self.client.logout()

    def test_post_request(self):
        task = Task.objects.get(pk=1)
        response = self.client.post(f'/{task.id}/update/', task_id=task.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/{task.id}/update/')

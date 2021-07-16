from django.test import TestCase
from django.urls import reverse
from user.models import User
from project.models.project import Project
from project.models.task import Task


class ProjectViewTest(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()

    def test_get_request_user_authenticate(self):
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(reverse('project:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/projects/projects.html')
        self.client.logout()
    
    def test_get_request_user_no_authenticate(self):
        response = self.client.get(reverse('project:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/dashboard/')

    def test_post_request_user_authenticate(self):
        project = Project.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:form_update_project', args=[project.id]), project_id=project.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], project)
        self.assertEqual(type(response.context['project']), Project)
        self.assertTemplateUsed(response, 'project/projects/forms/update_project.html')
        self.client.logout()

    def test_post_request(self):
        project = Project.objects.get(pk=1)
        response = self.client.post(reverse('project:form_update_project', args=[project.id]), project_id=project.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/{project.id}/update_form/')


class TaskViewTest(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()

    def test_get_request_user_authenticate(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(reverse('project:task', args=[project.id, task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/tasks/tasks.html')
        self.client.logout()

    def test_get_request_user_no_authenticate(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('project:task', args=[project.id, task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/project-{project.id}/task-{task.id}/')

    def test_post_request_user_authenticate(self):
        task = Task.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:form_update_task', args=[task.id]), task_id=task.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], task)
        self.assertEqual(type(response.context['task']), Task)
        self.assertTemplateUsed(response, 'project/tasks/forms/update_task.html')
        self.client.logout()

    def test_post_request(self):
        task = Task.objects.get(pk=1)
        response = self.client.post(reverse('project:form_update_task', args=[task.id]), task_id=task.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/{task.id}/update/')

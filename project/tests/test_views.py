from django.test import TestCase, override_settings
from django.urls import reverse
from user.models import User
from project.models.project import Project
from project.models.list import List
from project.models.task import Task
from timesheet.models.timesheet import Timesheet


class ProjectViewTest(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()

    def test_get_request_user_auth(self):
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(reverse('project:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/projects/projects.html')
        self.client.logout()
    
    def test_get_request_user_no_auth(self):
        response = self.client.get(reverse('project:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/dashboard/')

    def test_post_request_user_auth(self):
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

    def test_add_member_user_auth(self):
        project = Project.objects.get(pk=1)
        user = User.objects.get(pk=2)
        datas = {'member_email': user.email, 'project_name': project.id}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:add_member'), datas)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_name'], user.first_name)
        self.client.logout()

    def test_add_member(self):
        project = Project.objects.get(pk=1)
        user = User.objects.get(pk=2)
        datas = {'member_email': user.email, 'project_name': project.id}
        response = self.client.post(reverse('project:add_member'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/add_member/')

    def test_create_project_user_auth(self):
        datas = {'project_name': 'Test'}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:create_project'), datas)
        project = Project.objects.get(name='Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_name'], project.name)
        self.assertEqual(response.json()['project_id'], project.id)
        self.client.logout()

    def create_project_and_add_member(self):
        self.client.login(username='email@test.com', password='test_password_61')
        datas = {'project_name': 'Test'}
        response = self.client.post(reverse('project:create_project'), datas)
        project = Project.objects.get(name='Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_name'], project.name)
        self.assertEqual(response.json()['project_id'], project.id)

        user = User.objects.get(pk=2)
        datas = {'member_email': user.email, 'project_name': project.id}
        new_response = self.client.post(reverse('project:add_member'), datas)
        self.assertEqual(new_response.status_code, 200)
        self.assertJSONEqual(
            str(new_response.content, encoding='utf8'),
            {'user_name': user.first_name}
        )
        self.client.logout()

    def test_update_project_and_add_member(self):
        self.client.login(username='email@test.com', password='test_password_61')
        project = Project.objects.get(pk=1)
        datas = {'project_id': project.id, 'name': 'New project'}
        response = self.client.post(reverse('project:update_project'), datas)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_id'], project.id)

        user = User.objects.get(pk=2)
        datas_to_add_member = {'member_email': user.email, 'project_name': project.id}
        response = self.client.post(reverse('project:add_member'), datas_to_add_member)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_name'], user.first_name)
        self.client.logout()

    def test_create_project_and_update(self):
        self.client.login(username='email@test.com', password='test_password_61')
        datas = {'project_name': 'Test'}
        response = self.client.post(reverse('project:create_project'), datas)
        project = Project.objects.get(name='Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_name'], project.name)
        self.assertEqual(response.json()['project_id'], project.id)

        new_datas = {'project_id': project.id, 'name': 'New project'}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:update_project'), new_datas)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_id'], project.id)
        self.client.logout()

    def test_create_project(self):
        datas = {'project_name': 'Test'}
        response = self.client.post(reverse('project:create_project'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/create_project/')

    def test_delete_project_user_auth(self):
        project = Project.objects.get(pk=1)
        datas = {'project_id': project.id}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:delete_project'), datas)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_id'], str(project.id))
        self.client.logout()

    def test_delete_project(self):
        project = Project.objects.get(pk=1)
        datas = {'project_id': project.id}
        response = self.client.post(reverse('project:delete_project'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/delete_project/')

    def test_update_project_user_auth(self):
        project = Project.objects.get(pk=1)
        datas = {'project_id': project.id, 'name': 'New project'}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:update_project'), datas)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['project_id'], project.id)
        self.client.logout()
    
    def test_update_project(self):
        project = Project.objects.get(pk=1)
        datas = {'project_id': project.id, 'name': 'New project'}
        response = self.client.post(reverse('project:update_project'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/update_project/')

    def test_get_statistics_user_auth(self):
        project = Project.objects.get(pk=1)
        nb_task = Project.objects_project.get_number_task_by_list(project)
        time = Project.objects_project.get_total_planned_hours(project)
        history = Project.objects_project.get_history_time_work(project, List, Task, Timesheet)

        datas = {'project_id': project.id}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:get_statistics'), datas)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'nb_task': nb_task, 'time': time, 'history': history}
        )
        self.client.logout()

    def test_get_statistics(self):
        project = Project.objects.get(pk=1)
        response = self.client.post(reverse('project:get_statistics'), project_id=project.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/get_statistics/')


class ListViewTest(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()
    
    def test_get_request_user_auth(self):
        project = Project.objects.get(pk=1)
        
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(reverse('project:project', args=[project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], project)
        self.assertTemplateUsed(response, 'project/lists/lists.html')
        self.client.logout()

    def test_get_request(self):
        project = Project.objects.get(pk=1)
        response = self.client.get(reverse('project:project', args=[project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/project-{project.id}/')

    def test_post_request_user_auth(self):
        p_list = List.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:form_update_list', args=[p_list.id]), list_id=p_list.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list'], p_list)
        self.assertEqual(type(response.context['list']), List)
        self.assertTemplateUsed(response, 'project/lists/forms/update_list.html')
        self.client.logout()

    def test_post_request(self):
        p_list = List.objects.get(pk=1)
        response = self.client.post(reverse('project:form_update_list', args=[p_list.id]), list_id=p_list.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/{p_list.id}/update_list_form/')

    def test_create_list_user_auth(self):
        project = Project.objects.get(pk=1)
        datas = {'list_name': 'Cancel', 'project_id': project.id}

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:create_list'), datas)
        new_list = List.objects.get(name='Cancel')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['new_list'], new_list)
        self.assertEqual(response.json()['list_name'], new_list.name)
        self.assertEqual(response.json()['list_id'], new_list.id)
        self.client.logout()

    def test_create_list(self):
        project = Project.objects.get(pk=1)
        datas = {'list_name': 'Cancel', 'project_id': project.id}
        response = self.client.post(reverse('project:create_list'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/create_list/')

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_delete_list_user_auth(self):
        p_list = List.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:delete_list'), {'list_id': p_list.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['list_id'], str(p_list.id))
        self.assertEqual(response.json()['success'], 'The list has been deleted')
        self.client.logout()

    def test_delete_list(self):
        p_list = List.objects.get(pk=1)
        response = self.client.post(reverse('project:delete_list'), {'list_id': p_list.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/delete_list/')

    def test_create_task_user_auth(self):
        p_list = List.objects.get(pk=1)
        datas = {'task_name': 'Test', 'list_id': p_list.id}

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:create_task'), datas)
        new_task = Task.objects.get(name='Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['task_name'], new_task.name)
        self.assertEqual(response.json()['task_id'], new_task.id)
        self.assertEqual(response.json()['list_id'], str(p_list.id))
        self.client.logout()

    def test_create_task(self):
        p_list = List.objects.get(pk=1)
        datas = {'task_name': 'Test', 'list_id': p_list.id}

        response = self.client.post(reverse('project:create_task'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/create_task/')

    def test_update_list_user_auth(self):
        p_list = List.objects.get(pk=1)
        datas = {'list_id': p_list.id, 'name': 'Cancel'}
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:update_list'), datas)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'list_id': p_list.id, 'list_name': 'Cancel'}
        )
        self.client.logout()

    def test_update_list(self):
        p_list = List.objects.get(pk=1)
        datas = {'list_id': p_list.id, 'name': 'Cancel'}
        response = self.client.post(reverse('project:update_list'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/update_list/')


class TaskViewTest(TestCase):

    fixtures = ['datas.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('test_password_61')
        self.user.save()

    def test_get_request_user_auth(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.get(reverse('project:task', args=[project.id, task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/tasks/tasks.html')
        self.client.logout()

    def test_get_request_user_no_auth(self):
        project = Project.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('project:task', args=[project.id, task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/project-{project.id}/task-{task.id}/')

    def test_post_request_user_auth(self):
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

    def test_update_task_user_auth(self):
        task = Task.objects.get(pk=1)
        user = User.objects.get(pk=2)
        datas = {
            'task_id': task.id,
            'name': 'Test cancel',
            'assigned_to': user.id,
            'deadline': '10/07/2021',
            'planned_hours': '02:00',
            'created_at': '2021-06-29 00:00:00+02',
            'user': user.id,
            'description': 'a little description.',
            'timesheet_set-0-created_at': "10/07/2021",
            'timesheet_set-0-description': "ffff",
            'timesheet_set-0-id': "",
            'timesheet_set-0-task': "32",
            'timesheet_set-0-unit_hour': "02:00",
            'timesheet_set-0-user': "2",
            'timesheet_set-INITIAL_FORMS': "0",
            'timesheet_set-MAX_NUM_FORMS': "1000",
            'timesheet_set-MIN_NUM_FORMS': "0",
            'timesheet_set-TOTAL_FORMS': "1",
        }

        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:update_task'), datas)
        self.assertEqual(response.context['task'], task)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['task_id'], task.id)
        self.client.logout()

    def test_update_task(self):
        task = Task.objects.get(pk=1)
        user = User.objects.get(pk=2)
        datas = {
            'task_id': task.id,
            'name': 'Test cancel',
            'assigned_to': user.id,
            'deadline': '10/07/2021',
            'planned_hours': '02:00',
            'created_at': '2021-06-29 00:00:00+02',
            'user': user.id,
            'description': 'a little description.',
            'timesheet_set-0-created_at': "10/07/2021",
            'timesheet_set-0-description': "ffff",
            'timesheet_set-0-id': "",
            'timesheet_set-0-task': "32",
            'timesheet_set-0-unit_hour': "02:00",
            'timesheet_set-0-user': "2",
            'timesheet_set-INITIAL_FORMS': "0",
            'timesheet_set-MAX_NUM_FORMS': "1000",
            'timesheet_set-MIN_NUM_FORMS': "0",
            'timesheet_set-TOTAL_FORMS': "1",
        }
        response = self.client.post(reverse('project:update_task'), datas)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/update_task/')

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_delete_task_user_auth(self):
        task = Task.objects.get(pk=1)
        self.client.login(username='email@test.com', password='test_password_61')
        response = self.client.post(reverse('project:delete_task'), {'task_id': task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['task_id'], str(task.id))
        self.assertEqual(response.json()['success'], 'The task has been deleted')
        self.client.logout()

    def test_delete_task(self):
        task = Task.objects.get(pk=1)
        response = self.client.post(reverse('project:delete_task'), {'task_id': task.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/delete_task/')

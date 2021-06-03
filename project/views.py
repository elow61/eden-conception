""" All views for the user application """
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .forms import CreateProjectForm, CreateListForm, CreateTaskForm
from .models import Project, ProjectList, ProjectTask
from user.models import User


class DashboardView(View):

    template_name = 'project/dashboard.html'
    form = CreateProjectForm

    def get(self, request):
        context = {}
        context['form'] = self.form

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            projects = user.main_user.all()
            context['projects'] = projects

        return render(request, self.template_name, context)

    @staticmethod
    def create_project(request):
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                query = request.POST.get('project_name')
                user = User.objects.get(id=request.user.id)
                Project.objects.create(
                    name=query,
                    user=user,
                )
                projects = user.main_user.all()
                context['projects'] = projects

                res['project_name'] = query
                res['project_id'] = Project.objects.get(name=query).id
                res['template'] = render_to_string('project/project_detail.html', context, request=request)
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)

    @staticmethod
    def delete_project(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                project_id = request.POST.get('project_id')
                print(project_id)
                project_to_delete = Project.objects.get(id=project_id)
                project_to_delete.delete()

                res['project_id'] = project_id
                res['success'] = _('The project has deleted')
            else:
                res['error'] = _('The project doesn\'t have deleted')
        else:
            res['error'] = _('Please, connect you.')

        return JsonResponse(res)


class ProjectView(View):

    template_name = 'project/project.html'
    form = CreateListForm

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        lists = project.projectlist_set.all()

        context = {
            'project': project,
            'lists': lists,
            'create_list_form': self.form,
            'create_task_form': CreateTaskForm
        }
        return render(request, self.template_name, context)

    @staticmethod
    def create_list(request):
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST.get('list_name')
                project_id = request.POST.get('project_id')
                project = Project.objects.get(id=project_id)

                ProjectList.objects.create(
                    name=name,
                    project=project,
                )
                project.save()

                new_list = ProjectList.objects.get(name=name)
                context['new_list'] = new_list

                res['list_name'] = name
                res['list_id'] = new_list.id
                res['template'] = render_to_string('project/project_list.html', context, request=request)
            else:
                res['error'] = _('Please, write a list name.')
        else:
            res['error'] = _('Connect before create a list')

        return JsonResponse(res)

    @staticmethod
    def delete_list(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                list_id = request.POST.get('list_id')
                list_to_delete = ProjectList.objects.get(id=list_id)
                project = Project.objects.get(id=list_to_delete.project_id)

                list_to_delete.delete()
                project.save()

                res['list_id'] = list_id
                res['success'] = _('The list has deleted')
            else:
                res['error'] = _('The list doesn\'t have deleted')
        else:
            res['error'] = _('Please, connect you.')

        return JsonResponse(res)

    @staticmethod
    def create_task(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST.get('task_name')
                list_id = request.POST.get('list_id')
                current_list = ProjectList.objects.get(id=int(list_id))
                project = Project.objects.get(id=current_list.project_id)

                ProjectTask.objects.create(
                    name=name,
                    project_list=current_list,
                )
                project.save()

                task = ProjectTask.objects.get(name=name)
                context = {'task': task}

                res['task_name'] = name
                res['task_id'] = task.id
                res['list_id'] = list_id
                res['template'] = render_to_string('project/project_task.html', context)

        return JsonResponse(res)

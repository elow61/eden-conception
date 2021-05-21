""" All views for the user application """
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .forms import CreateProjectForm, CreateListForm
from .models import Project, ProjectList
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
                res['template'] = render_to_string('project/project_detail.html', context)
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)


class ProjectView(View):

    template_name = 'project/project.html'
    form = CreateListForm

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        lists = project.projectlist_set.all()
        context = {'project': project, 'lists': lists, 'form': self.form}
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

                new_list = ProjectList.objects.get(name=name)
                context['new_list'] = new_list

                res['list_name'] = name
                res['list_id'] = new_list.id
                res['template'] = render_to_string('project/project_list.html', context)
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
                list_to_delete.delete()

                res['success'] = _('The list has deleted')
            else:
                res['error'] = _('The list doesn\'t have deleted')
        else:
            res['error'] = _('Please, connect you.')

        return JsonResponse(res)

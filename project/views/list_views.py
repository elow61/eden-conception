""" All views for the user application """
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.forms.list_forms import CreateListForm
from project.forms.task_forms import CreateTaskForm
from project.models.project import Project
from project.models.list import List
from project.models.task import Task
from user.models import User


class ListView(View):

    template_name = 'project/lists/lists.html'
    form = CreateListForm

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        lists = project.list_set.all()

        context = {
            'project': project,
            'lists': lists,
            'create_list_form': self.form,
            'create_task_form': CreateTaskForm
        }
        return render(request, self.template_name, context)

    @classmethod
    def create_list(cls, request):
        res = {}
        context = {}
        form = cls.form(request.POST)
        print(request)
        if form.is_valid():
            name = form.cleaned_data['list_name']

            project_id = request.POST.get('project_id')
            project = Project.objects.get(id=project_id)

            new_list = List.objects.create(
                name=name,
                project=project,
            )
            project.save()

            context['new_list'] = new_list
            context['create_task_form'] = CreateTaskForm

            res['list_name'] = name
            res['list_id'] = new_list.id
            res['template'] = render_to_string('project/lists/new_list.html', context, request=request)
        else:
            res['error'] = _('Please, write a list name.')

        return JsonResponse(res)

    @staticmethod
    def delete_list(request):
        res = {}
        if request.method == 'POST':
            list_id = request.POST.get('list_id')
            list_to_delete = List.objects.get(id=list_id)
            project = Project.objects.get(id=list_to_delete.project_id)

            list_to_delete.delete()
            project.save()

            res['list_id'] = list_id
            res['success'] = _('The list has deleted')
        else:
            res['error'] = _('The list doesn\'t have deleted')

        return JsonResponse(res)

    @staticmethod
    def create_task(request):
        res = {}
        if request.method == 'POST':
            user = User.objects.get(id=request.user.id)
            name = request.POST.get('task_name')
            list_id = request.POST.get('list_id')
            current_list = List.objects.get(id=int(list_id))
            project = Project.objects.get(id=current_list.project_id)

            index = Task.objects_task.get_index(current_list)
            new_task = Task.objects.create(
                name=name,
                project_list=current_list,
                assigned_to=user,
                deadline=None,
                index=index,
                planned_hours=0.0,
            )
            project.save()

            context = {'task': new_task, 'project': project}

            res['task_name'] = name
            res['task_id'] = new_task.id
            res['list_id'] = list_id
            res['template'] = render_to_string('project/tasks/new_task.html', context)

        return JsonResponse(res)

    @staticmethod
    def update_order_task(request):
        res = {}
        if request.method == 'POST':
            datas = json.loads(request.POST.get('datas'))
            Task.objects_task.update_order_task(datas)

        return JsonResponse(res)

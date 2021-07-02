""" All views for the user application """
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import F
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.forms.task_forms import UpdateTaskForm
from project.models.project import Project
from project.models.task import Task
from user.models import User
from timesheet.models.timesheet import Timesheet
from timesheet.forms.timesheet_forms import UpdateTimesheetForm


class TaskView(View):

    template_name = 'project/tasks/tasks.html'

    def get(self, request, project_id, task_id):
        project = get_object_or_404(Project, pk=project_id)
        task = get_object_or_404(Task, pk=task_id)
        context = {'project': project, 'task': task}

        return render(request, self.template_name, context)

    def post(self, request, task_id):
        ''' Method to display the form to update one task '''
        res = {}
        if request.method == 'POST':
            task_id = request.POST.get('task_id')
            current_task = Task.objects.get(id=int(task_id))
            datas = {}
            datas['name'] = current_task.name
            datas['assigned_to'] = current_task.assigned_to
            datas['deadline'] = current_task.deadline
            datas['description'] = current_task.description
            datas['planned_hours'] = current_task.planned_hours

            form_update = UpdateTaskForm(instance=current_task, initial=datas)
            TimeFormSet = inlineformset_factory(
                parent_model=Task,
                model=Timesheet,
                form=UpdateTimesheetForm,
                can_delete=True,
                extra=1,
                fields=('created_at', 'user', 'description', 'unit_hour')
            )
            formset = TimeFormSet(instance=current_task)
            context = {'form_update': form_update, 'formset': formset, 'task': current_task}

            res['task_id'] = task_id
            res['template'] = render_to_string('project/tasks/forms/update_task.html', context, request=request)

        return JsonResponse(res)

    @staticmethod
    def update_task(request):
        res = {}
        TimeFormSet = inlineformset_factory(
            parent_model=Task,
            model=Timesheet,
            form=UpdateTimesheetForm,
            can_delete=True,
        )
        if request.method == 'POST':
            user = User.objects.get(id=request.POST.get('assigned_to'))
            date_object = datetime.strptime(request.POST.get('deadline'), '%d/%m/%Y')
            current_task = Task.objects.get(id=request.POST.get('task_id'))

            formset = TimeFormSet(request.POST, instance=current_task)

            if formset.is_valid():
                formset.save()

            # Convert time to float
            convert_in_time = datetime.strptime(request.POST.get('planned_hours'), '%H:%M').time()
            planned_hours_float = convert_in_time.hour + convert_in_time.minute / 60.0

            current_task.name = request.POST.get('name')
            current_task.assigned_to = user
            current_task.deadline = date_object
            current_task.description = request.POST.get('description')
            current_task.planned_hours = planned_hours_float
            current_task.save()

            context = {'task': current_task}

            res['task_id'] = current_task.id
            res['template'] = render_to_string('project/tasks/task_detail.html', context)

        return JsonResponse(res)

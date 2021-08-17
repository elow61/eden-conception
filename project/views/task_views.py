""" All views for the model task """
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.forms.task_forms import UpdateTaskForm
from project.models.project import Project
from project.models.task import Task
from user.models import User
from timesheet.views.timesheet_views import TimesheetView


class TaskView(View):
    ''' Class to manage all interactions and views with the tasks. '''
    template_name = 'project/tasks/tasks.html'

    def get(self, request, project_id, task_id):
        ''' Method to view the detail of a task. '''
        project = get_object_or_404(Project, pk=project_id)
        task = get_object_or_404(Task, pk=task_id)
        context = {'project': project, 'task': task}

        return render(request, self.template_name, context)

    def post(self, request, task_id):
        ''' Method to display the form to update one task '''
        res = {}
        if request.method == 'POST':
            current_task = Task.objects.get(id=task_id)
            datas = {
                'name': current_task.name,
                'assigned_to': current_task.assigned_to,
                'deadline': current_task.deadline,
                'description': current_task.description,
                'planned_hours': current_task.planned_hours
            }

            form_update = UpdateTaskForm(instance=current_task, initial=datas)
            context = {
                'form_update': form_update,
                'formset': TimesheetView.create_formset(current_task),
                'task': current_task
            }

            res['task_id'] = task_id
            res['template'] = render_to_string(
                template_name='project/tasks/forms/update_task.html',
                context=context,
                request=request
            )

        return JsonResponse(res)

    @staticmethod
    def update_task(request):
        ''' Method to update a task. '''
        res = {}
        if request.method == 'POST':
            current_task = Task.objects.get(id=request.POST.get('task_id'))
            formset = TimesheetView.update_timesheet(request)

            if formset is not True:
                formset_clean = [i for i in formset if i]
                if formset_clean:
                    res['error'] = formset_clean[0]

            # Convert time to float
            convert_in_time = datetime.strptime(request.POST.get('planned_hours'), '%H:%M').time()
            planned_hours_float = convert_in_time.hour + convert_in_time.minute / 60.0

            # Update task
            current_task.name = request.POST.get('name')
            current_task.assigned_to = User.objects.get(id=request.POST.get('assigned_to'))
            current_task.deadline = datetime.strptime(request.POST.get('deadline'), '%d/%m/%Y')
            current_task.description = request.POST.get('description')
            current_task.planned_hours = planned_hours_float
            current_task.save()

            context = {'task': current_task}

            res['task_id'] = current_task.id
            res['template'] = render_to_string('project/tasks/task_detail.html', context)

        return JsonResponse(res)

    @staticmethod
    def delete_task(request):
        ''' Method to delete a task. '''
        res = {}
        if request.method == 'POST':
            task_to_delete = Task.objects.get(id=request.POST.get('task_id'))
            project = Project.objects.get(id=task_to_delete.project_list.project_id)

            task_to_delete.delete()
            project.save()

            res['task_id'] = request.POST.get('task_id')
            res['project_id'] = project.id
            res['success'] = _('The task has been deleted')
        else:
            res['error'] = _('The task doesn\'t have deleted')

        return JsonResponse(res)

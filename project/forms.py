from django import forms
from django.forms import ModelForm, DateField, TimeInput
from django.utils.translation import gettext_lazy as _
from .models import Task


class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label=_('Project name'), max_length=100)


class CreateListForm(forms.Form):
    list_name = forms.CharField(label=_('List name'), max_length=100)


class CreateTaskForm(forms.Form):
    task_name = forms.CharField(label=_('Task name'), max_length=100)


class UpdateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'assigned_to', 'deadline', 'description', 'planned_hours']
        widget = {
            'deadline': DateField(input_formats=['%d-%m-%Y']),
            'planned_hours': TimeInput(format=['%H:%M']),
        }

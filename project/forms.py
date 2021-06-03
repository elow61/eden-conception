from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Project


class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label=_('Project name'), max_length=100)


class CreateListForm(forms.Form):
    list_name = forms.CharField(label=_('List name'), max_length=100)


class CreateTaskForm(forms.Form):
    task_name = forms.CharField(label=_('Task name'), max_length=100)
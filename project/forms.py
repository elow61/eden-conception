from django import forms
from django.forms import ModelForm, DateField, TimeInput
from django.utils.translation import gettext_lazy as _
from .models import Project, List, Task
from user.models import User


class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label=_('Project name'), max_length=100)


class CreateListForm(forms.Form):
    list_name = forms.CharField(label=_('List name'), max_length=100)


class CreateTaskForm(forms.Form):
    task_name = forms.CharField(label=_('Task name'), max_length=100)


class UpdateTaskForm(ModelForm):

    def __init__(self, instance, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        project = List.objects.get(pk=instance.project_list.id).project
        self.fields['assigned_to'] = forms.ModelChoiceField(queryset=project.user_ids.all(), empty_label=None)

    class Meta:
        model = Task
        fields = ['name', 'assigned_to', 'deadline', 'description', 'planned_hours']
        widget = {
            'deadline': DateField(input_formats=['%d-%m-%Y']),
            'planned_hours': TimeInput(format=['%H:%M']),
        }


class AddMember(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(AddMember, self).__init__(*args, **kwargs)
        user = User.objects.get(id=request.user.id)
        projects = user.main_user.all()
        self.fields['project_name'] = forms.ModelChoiceField(queryset=projects, empty_label=None)

    member_email = forms.CharField(label=_('Member Email'), max_length=100)

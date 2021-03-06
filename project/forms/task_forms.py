''' Forms to the model Task '''
from django import forms
from django.forms import ModelForm, DateField
from django.utils.translation import gettext_lazy as _
from project.models.list import List
from project.models.task import Task
from .widgets import HourField


class CreateTaskForm(forms.Form):
    ''' Form to create a task '''
    task_name = forms.CharField(label=_('Task name'), max_length=100)


class UpdateTaskForm(ModelForm):
    ''' Form to update a task '''
    deadline = DateField(input_formats=['%d/%m/%Y'], required=True, label=_('Deadline'))

    def __init__(self, instance, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        project = List.objects.get(pk=instance.project_list.id).project
        self.fields['assigned_to'] = forms.ModelChoiceField(
            queryset=project.user_ids.all(),
            empty_label=None,
            label=_('Assigned to')
        )
        self.fields['planned_hours'] = HourField(label=_('Planned hours'))

    class Meta:
        ''' Class Meta is used to target the model and her fields '''

        model = Task
        fields = ['name', 'assigned_to', 'deadline', 'description', 'planned_hours']

''' Forms for the model Timesheet '''
from django import forms
from django.forms import ModelForm, DateField
from project.models.list import List
from timesheet.models.timesheet import Timesheet
from project.forms.widgets import HourField
from django.utils.translation import gettext_lazy as _


class UpdateTimesheetForm(ModelForm):
    ''' Form to update the timesheets or create into a task '''
    created_at = DateField(input_formats=['%d/%m/%Y'], required=True, label=_('Created at'))

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop('current_task')
        super(UpdateTimesheetForm, self).__init__(*args, **kwargs)
        
        self.fields['unit_hour'] = HourField(label=_('Unit hour'))
        self.fields['unit_hour'].widget.attrs['placeholder'] = '00:00'
        self.fields['user'] = forms.ModelChoiceField(
            queryset=List.objects.filter(id=self.task.project_list.id).first().project.user_ids.all(),
            label=_('User')
        )

    class Meta:
        ''' Is used to target the model and her field '''
        model = Timesheet
        fields = ['created_at', 'user', 'description', 'unit_hour']

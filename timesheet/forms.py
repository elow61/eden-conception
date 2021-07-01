from django import forms
from django.forms import ModelForm, DateField, TimeInput, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from .models import Timesheet
from project.models import List
from project.widget import HourField


class UpdateTimesheetForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateTimesheetForm, self).__init__(*args, **kwargs)
        self.fields['unit_hour'] = HourField()

    class Meta:
        model = Timesheet
        fields = ['created_at', 'user', 'description', 'unit_hour']
        widget = {
            'created_at': DateField(input_formats=['%d-%m-%Y']),
        }

from django import forms
from django.forms import ModelForm, DateField, TimeInput, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from .models import Timesheet
from user.models import User


class UpdateTimesheetForm(ModelForm):

    class Meta:
        model = Timesheet
        fields = ['created_at', 'user', 'description', 'unit_hour']
        widget = {
            'created_at': DateField(input_formats=['%d-%m-%Y']),
            'unit_hour': TimeInput(format=['%H:%M']),
        }

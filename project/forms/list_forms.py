''' Forms for model List '''
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from project.models.list import List


class CreateListForm(forms.Form):
    ''' Form to create a List '''
    list_name = forms.CharField(label=_('List name'), max_length=100)


class UpdateListForm(ModelForm):
    ''' Form to update the list's name '''

    class Meta:
        ''' Class Meta is used to target the model and her field '''
        model = List
        fields = ['name']

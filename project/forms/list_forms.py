from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from project.models.list import List


class CreateListForm(forms.Form):
    list_name = forms.CharField(label=_('List name'), max_length=100)


class UpdateListForm(ModelForm):

    class Meta:
        model = List
        fields = ['name']

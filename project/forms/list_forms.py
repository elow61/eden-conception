from django import forms
from django.utils.translation import gettext_lazy as _


class CreateListForm(forms.Form):
    list_name = forms.CharField(label=_('List name'), max_length=100)

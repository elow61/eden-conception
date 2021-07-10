from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from user.models import User
from project.models.project import Project


class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label=_('Project name'), max_length=100)


class AddMember(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(AddMember, self).__init__(*args, **kwargs)
        user = User.objects.get(id=request.user.id)
        projects = user.main_user.all()
        self.fields['project_name'] = forms.ModelChoiceField(queryset=projects, empty_label=None)

    member_email = forms.CharField(label=_('Member Email'), max_length=100)


class UpdateProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name']

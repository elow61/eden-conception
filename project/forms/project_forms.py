''' Forms to the model Project '''
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from user.models import User
from project.models.project import Project


class CreateProjectForm(forms.Form):
    ''' Form used to create a project '''
    project_name = forms.CharField(label=_('Project name'), max_length=100)


class AddMember(forms.Form):
    ''' From used to add a member into a project '''

    def __init__(self, request, *args, **kwargs):
        super(AddMember, self).__init__(*args, **kwargs)
        user = User.objects.get(id=request.user.id)
        projects = user.main_user.all()
        self.fields['project_name'] = forms.ModelChoiceField(queryset=projects, empty_label=None)

    member_email = forms.CharField(label=_('Member Email'), max_length=100)


class UpdateProjectForm(ModelForm):
    ''' Form used to update the project's name '''

    class Meta:
        ''' Class Meta is used to target the model and her field '''
        model = Project
        fields = ['name']

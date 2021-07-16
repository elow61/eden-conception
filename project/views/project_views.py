""" All views for the user application """
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.forms.project_forms import CreateProjectForm, AddMember, UpdateProjectForm
from project.models.project import Project
from user.models import User


class ProjectView(View):

    template_name = 'project/projects/projects.html'
    form = CreateProjectForm

    def get(self, request):
        context = {}
        context['form'] = self.form
        context['form_add_member'] = AddMember(request)

        user = User.objects.get(id=request.user.id)
        projects = user.main_user.all()
        context['projects'] = projects

        return render(request, self.template_name, context)

    def post(self, request, project_id):
        ''' Method to display the form to update a project '''
        res = {}
        if request.method == 'POST':
            current_project = Project.objects.get(id=project_id)
            datas = {'name': current_project.name}

            form_update = UpdateProjectForm(instance=current_project, initial=datas)
            context = {'form_update': form_update, 'project': current_project}
            res['project_id'] = project_id
            res['template'] = render_to_string('project/projects/forms/update_project.html', context, request=request)

        return JsonResponse(res)

    @staticmethod
    def add_member(request):
        res = {}
        if request.method == 'POST':
            query = request.POST.get('member_email')
            project = Project.objects.get(pk=request.POST.get('project_name'))
            new_user = Project.objects_project.add_member(query, project)

            if new_user:
                res['user_name'] = new_user.get().first_name
            else:
                res['error'] = _('No user email saved in database')

        return JsonResponse(res)

    @staticmethod
    def create_project(request):
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                query = request.POST.get('project_name')
                user = User.objects.get(id=request.user.id)
                Project.objects.create(
                    name=query,
                    user=user,
                )
                project = Project.objects.get(name=query)
                project.user_ids.add(user.id)
                projects = user.main_user.all()

                context['projects'] = projects

                res['project_name'] = query
                res['project_id'] = project.id
                res['template'] = render_to_string('project/projects/project_detail.html', context, request=request)
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)

    @staticmethod
    def delete_project(request):
        res = {}
        if request.method == 'POST':
            project_id = request.POST.get('project_id')
            project_to_delete = Project.objects.get(id=project_id)
            project_to_delete.delete()

            res['project_id'] = project_id
            res['success'] = _('The project has deleted')
        else:
            res['error'] = _('The project doesn\'t have deleted')

        return JsonResponse(res)

    @staticmethod
    def update_project(request):
        res = {}
        if request.method == 'POST':
            current_project = Project.objects.get(id=request.POST.get('project_id'))

            # Update project
            current_project.name = request.POST.get('name')
            current_project.save()

            res['project_id'] = current_project.id
            res['project_name'] = current_project.name

        return JsonResponse(res)


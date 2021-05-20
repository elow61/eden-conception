""" All views for the user application """
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .forms import CreateProjectForm
from .models import Project
from user.models import User


class DashboardView(View):

    template_name = 'project/dashboard.html'
    form = CreateProjectForm

    def get(self, request):
        context = {}
        context['form'] = self.form

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            projects = user.main_user.all()
            context['projects'] = projects

        return render(request, self.template_name, context)

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
                projects = user.main_user.all()
                context['projects'] = projects

                res['product_name'] = query
                res['product_id'] = Project.objects.get(name=query).id
                res['template'] = render_to_string('project/project_detail.html', context)
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)


class ProjectView(View):

    template_name = 'project/project.html'

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        context = {'project': project}
        return render(request, self.template_name, context)

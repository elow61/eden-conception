from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from . import views


app_name = 'project'

urlpatterns = [
    path('dashboard/', login_required(views.ProjectView.as_view()), name='dashboard'),
    path('create_project/', login_required(views.ProjectView.create_project), name='create_project'),
    path('delete_project/', login_required(views.ProjectView.delete_project), name='delete_project'),

    path('project-<int:project_id>/', login_required(views.ListView.as_view()), name='project'),
    path('create_list/', login_required(views.ListView.create_list), name='create_list'),
    path('delete_list/', login_required(views.ListView.delete_list), name='delete_list'),

    path('create_task/', login_required(views.ListView.create_task), name='create_task'),
    path('project-<int:project_id>/task-<int:task_id>/', login_required(views.TaskView.as_view()), name='task'),
]

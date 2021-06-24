from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from . import views


app_name = 'project'

urlpatterns = [
    path('dashboard/', login_required(views.ProjectView.as_view(), login_url='user:login'), name='dashboard'),
    path('create_project/', login_required(views.ProjectView.create_project, login_url='user:login'), name='create_project'),
    path('delete_project/', login_required(views.ProjectView.delete_project, login_url='user:login'), name='delete_project'),
    path('add_member/', login_required(views.ProjectView.add_member, login_url='user:login'), name='add_member'),

    path('project-<int:project_id>/', login_required(views.ListView.as_view(), login_url='user:login'), name='project'),
    path('create_list/', login_required(views.ListView.create_list, login_url='user:login'), name='create_list'),
    path('delete_list/', login_required(views.ListView.delete_list, login_url='user:login'), name='delete_list'),
    path('create_task/', login_required(views.ListView.create_task, login_url='user:login'), name='create_task'),
    path('update_order_task/', login_required(views.ListView.update_order_task, login_url='user:login'), name='update_task'),

    path('project-<int:project_id>/task-<int:task_id>/', login_required(views.TaskView.as_view(), login_url='user:login'), name='task'),
    path('<task_id>/update/', login_required(views.TaskView.as_view(), login_url='user:login'), name='form_update_task'),
    path('update_task/', login_required(views.TaskView.update_task, login_url='user:login'), name='update_task'),
]

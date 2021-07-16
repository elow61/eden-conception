from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from project.views.project_views import ProjectView
from project.views.list_views import ListView
from project.views.task_views import TaskView


app_name = 'project'

urlpatterns = [
    path('dashboard/', login_required(ProjectView.as_view(), login_url='user:login'), name='dashboard'),
    path('create_project/', login_required(ProjectView.create_project, login_url='user:login'), name='create_project'),
    path('delete_project/', login_required(ProjectView.delete_project, login_url='user:login'), name='delete_project'),
    path('add_member/', login_required(ProjectView.add_member, login_url='user:login'), name='add_member'),
    path('update_project/', login_required(ProjectView.update_project, login_url='user:login'), name='update_project'),
    path('<project_id>/update_form/', login_required(ProjectView.as_view(), login_url='user:login'), name='form_update_project'),

    path('project-<int:project_id>/', login_required(ListView.as_view(), login_url='user:login'), name='project'),
    path('create_list/', login_required(ListView.create_list, login_url='user:login'), name='create_list'),
    path('delete_list/', login_required(ListView.delete_list, login_url='user:login'), name='delete_list'),
    path('create_task/', login_required(ListView.create_task, login_url='user:login'), name='create_task'),
    path('update_order_task/', login_required(ListView.update_order_task, login_url='user:login'), name='update_task'),

    path('project-<int:project_id>/task-<int:task_id>/', login_required(TaskView.as_view(), login_url='user:login'), name='task'),
    path('<task_id>/update/', login_required(TaskView.as_view(), login_url='user:login'), name='form_update_task'),
    path('update_task/', login_required(TaskView.update_task, login_url='user:login'), name='update_task'),
]

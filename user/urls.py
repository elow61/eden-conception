# django.contrib.auth import urls
from django.db.models import base
from django.urls import path, include
from django.contrib.auth import views as v
from . import views


app_name = 'user'
urlpatterns = [
    path('login/', v.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', v.LogoutView.as_view()),

    path('register/', views.RegisterView.as_view(), name='register'),
]

from django.urls import path, include
from django.contrib.auth import views as v
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
]

""" All urls for the static_page application """
from django.urls import path
from . import views


app_name = 'static_page'
urlpatterns = [
    path('', views.IndexView.as_view(), name='homepage'),
    path('legal-notices/', views.LegalNoticeView.as_view(), name="legal_notices")
]

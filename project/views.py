""" All views for the user application """
from django.shortcuts import render, redirect
from django.views import View


class DashboardView(View):

    template_name = 'project/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)

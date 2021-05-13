""" All views for the user application """
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterView(View):

    template_name = 'user/register.html'
    form_class = UserCreationForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

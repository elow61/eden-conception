""" All views for the user application """
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from .forms import UserCreationFormInherit
from .models import User


class RegisterView(View):

    template_name = 'user/register.html'
    form_class = UserCreationFormInherit

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            user = User.objects.filter(email=email)
            if not user.exists():
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
            else:
                user = user.first()

            login(request, user)

            return redirect('project:dashboard')

        return render(request, self.template_name, {'form': form})

""" All views for the user application """
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.core.files.storage import default_storage
from .forms import UserCreationFormInherit
from .models import User


class RegisterView(View):

    template_name = 'user/register.html'
    form_class = UserCreationFormInherit

    def get(self, request):
        ''' Method to display the page contains the register form '''
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        ''' Method to manage the submit register form '''
        if request.method == 'POST':
            if 'image' in request.FILES:
                form = self.form_class(request.POST, request.FILES)
            else:
                form = self.form_class(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']

                user = User.objects.filter(email=email)
                if not user.exists():
                    if request.FILES:
                        file = request.FILES['image']
                        image = default_storage.save(file.name, file)
                        user = User.objects.create_user(
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            image=image,
                            email=email,
                            password=password1,
                        )
                    else:
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

        return render(
            request,
            self.template_name,
            {'form': self.form_class(request.POST, request.FILES)}
        )


class LogoutView(LogoutView):
    """ Class View to deconnect user """

    def get(self, request):
        logout(request)

        return redirect('user:login')

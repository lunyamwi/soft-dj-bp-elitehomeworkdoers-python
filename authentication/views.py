from django.views.generic import CreateView, FormView
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.mail import send_mail
from .models import User,Notification
from .forms import UserSignupForm, UserLoginForm,ClientSignupForm,WriterSignupForm


class UserRegistrationCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class = UserSignupForm
    template_name = 'authenticate/register.html'

    def post(self, request):
        """
        Overide the default post()
        """
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        data = {
            "first_name": form.cleaned_data['first_name'],
            "last_name": form.cleaned_data['last_name'],
            "password": form.cleaned_data['password'],
            "email": form.cleaned_data['email'].lower(),
            "date_of_birth": form.cleaned_data['date_of_birth'],
        }
        User.objects.create_user(**data)
        return redirect(reverse('authentication:login'))

class ClientRegistrationCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class =ClientSignupForm
    template_name = 'authenticate/register.html'

    def post(self, request):
        """
        Overide the default post()
        """
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        data = {
            "first_name": form.cleaned_data['first_name'],
            "last_name": form.cleaned_data['last_name'],
            "password": form.cleaned_data['password'],
            "email": form.cleaned_data['email'].lower(),
            "date_of_birth": form.cleaned_data['date_of_birth'],
        }
        User.objects.create_user(**data)
        return redirect(reverse('authentication:login'))

class WriterRegistrationCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class = WriterSignupForm
    template_name = 'authenticate/register.html'

    def post(self, request):
        """
        Overide the default post()
        """
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        data = {
            "first_name": form.cleaned_data['first_name'],
            "last_name": form.cleaned_data['last_name'],
            "password": form.cleaned_data['password'],
            "email": form.cleaned_data['email'].lower(),
            "date_of_birth": form.cleaned_data['date_of_birth'],
        }
        User.objects.create_user(**data)
        return redirect(reverse('authentication:login'))



class UserLoginCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class = UserLoginForm
    template_name = 'authenticate/login.html'
    success_url = reverse_lazy("index")

    def post(self, request):
        """
        Overide the default post()
        # """
        form = self.form_class(request.POST)
        email = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            return super(UserLoginCreateView, self).form_valid(form)
        messages.success(request, 'This email and password combination is invalid', extra_tags='red')
        return render(request, self.template_name, {"form": form})


def logout_view(request):
    logout(request)
    return redirect('authentication:login')


def show_notification(request,notification_id):
    n=Notification.objects.get(id=notification_id)
    return render(request,'notification.html',{'notification':n})


def delete_notification(request,notification_id):
    n=Notification.objects.get(id=notification_id)
    n.viewed=True
    n.save()
    return redirect('/')


def profile_view(request):
    context={}
    context['user']=User.objects.get(id=request.user.id)
    return render(request,'profile.html',context)
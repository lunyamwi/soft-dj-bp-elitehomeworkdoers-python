import stripe
import json
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView,CreateView
from django.views.generic import TemplateView

from assignments.models import Assignments
from assignments.filters import AssignmentFilter
from authentication.models import User,Notification
from payments.models import UserMembership
from .forms import ComposeForm
from .models import Thread, ChatMessage

stripe.api_key = settings.STRIPE_SECRET_KEY # new


class IndexView(TemplateView):
    template_name = "search.html"



class ClientView(TemplateView):
    template_name = "chat/clients.html"
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class WriterView(LoginRequiredMixin, ListView):
    template_name = "chat/writers.html"
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)




class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = None

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['form'] = self.get_form()
        # add the dictionary during initialization
        data = Assignments.objects.all().first()
        
        user_membership=UserMembership.objects.filter(user=self.request.user).first()
        # if user_membership:
        # if user_membership is not None:
        # import pdb; pdb.set_trace()
        user_membership_type=user_membership.membership.membership_type

        assignment_allowed_memberships=data.allowed_memberships.all() 

        context["data"] = None
        # if user_membership_type is not None

        if assignment_allowed_memberships.filter(membership_type=user_membership_type).exists():
            context['data'] = data

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
       return '{}'.format(reverse('chat:threads', kwargs={'username': self.kwargs.get('username')}))



def index(request):
    return render(request, 'chat/base.html', {})


@login_required
def room(request,room_name={'room_name':'support'}):
    # add the dictionary during initialization
    assignment_list = Assignments.objects.all()
    assignment_filter = AssignmentFilter(request.GET, queryset=assignment_list)
    if request.user.is_authenticated:
        notifications=Notification.objects.filter(user=request.user,viewed=False)

    return render(request,'chat/clients.html',{
        'room_name_json':mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username)),
        'filter':assignment_filter
    })
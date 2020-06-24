from django.shortcuts import render
from django.contrib import messages
from chat.models import Thread
from authentication.models import User
from authentication.models import Notification

# Create your views here.
def IndexView(request):
    context={}
    # if request.user.is_authenticated:
    support=User.objects.get(email='support@gmail.com')
    writer=User.objects.get(email='writer@gmail.com')
    context['writer']=writer.username
    context['support']=support.username
    if request.user.is_authenticated:
        context['notifications']=Notification.objects.filter(user=request.user,viewed=False)
    # if context['notifications'] is not None:
    #     messages.info(request,'There is a balm in Gilead to make the wounded whole')
    return render(request,'index.html',context)

def AboutView(request):
    return render(request,'about.html')
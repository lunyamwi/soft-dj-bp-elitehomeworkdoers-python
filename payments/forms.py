from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

# from .models import User,Client,Writer,Adminstration


# class ClientSignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model=User
    
#     @transaction.atomic
#     def save(self):
#         user=super.save(commit=False)
#         user.user_type=1
#         user.save()
#         Client.objects.create(user=user)
#         return user


# class WriterSignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model=User
    
#     @transaction.atomic
#     def save(self):
#         user=super.save(commit=False)
#         user.user_type=2
#         user.save()
#         Writer.objects.create(user=user)
#         return user


# class AdministrationSignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model=User
    
#     @transaction.atomic
#     def save(self):
#         user=super.save(commit=False)
#         user.user_type=1
#         user.save()
#         Adminstration.objects.create(user=user)
#         return user
from django.db import models
from django_countries.fields import CountryField
from .choices import ASSIGNMENT_LEVELS,ASSIGNMENT_TYPES
from django.conf import settings
# Create your models here.
from payments.models import Membership


class Assignments(models.Model):
    slug=models.SlugField(null=True)
    level = models.CharField(max_length=20,choices=ASSIGNMENT_LEVELS)
    types = models.CharField(max_length=20,choices=ASSIGNMENT_TYPES)
    country = CountryField()
    description=models.CharField(verbose_name='course_description',max_length=255,blank=True)
    document=models.FileField(upload_to='documents/',null=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    deadline=models.DateTimeField()
    is_approved=models.BooleanField(default=False)
    is_completed=models.BooleanField(default=False)
    revise=models.BooleanField(default=False)
    allowed_memberships=models.ManyToManyField(Membership)
    solution_format=models.CharField(max_length=200,null=True,blank=True)
    more_info=models.TextField('More Information Section',max_length=1200,null=True)

    def __str__(self):
        return self.description



class Writer(models.Model):
    slug=models.SlugField(null=True)
    title=models.CharField(max_length=120)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='writers')
    assignments=models.ManyToManyField(Assignments)

    def __str__(self):
        return self.user.username


    


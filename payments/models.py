import stripe
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

stripe.api_key=settings.STRIPE_SECRET_KEY


MEMBERSHIP_CHOICES=(
    ('Free','FREE'),
    ('Q1','Quote_One'),
    ('Q2','Quote Two'),
    ('Q3','Qutoe Three'),
)


    
class Membership(models.Model):
    slug=models.SlugField()
    membership_type=models.CharField(max_length=54,choices=MEMBERSHIP_CHOICES,default='Free')
    price=models.IntegerField(default=12)
    payment_status=models.BooleanField(default=False)
    stripe_plan_id=models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type 


class UserMembership(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=40)
    membership=models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True,default=4)

    # def __str__(self):
    #     return self.user
        

def post_save_usermembership_create(sender,instance,created,*args,**kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)   

    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id=='':
        new_customer_id=stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id=new_customer_id['id']
        user_membership.save()

post_save.connect(post_save_usermembership_create,sender=settings.AUTH_USER_MODEL)




class Subscription(models.Model):
    user_membership=models.ForeignKey(UserMembership,on_delete=models.CASCADE)
    stripe_subscription_id=models.CharField(max_length=40)
    active=models.BooleanField(default=True)

    def  __str__(self):
        return self.user_membership.user.username


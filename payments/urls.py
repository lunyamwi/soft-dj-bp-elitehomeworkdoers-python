from django.urls import path,include
from .views import (
    PaymentIndexView,
    HomePageView,
    charge,
    MembershipSelectView,
    PaymentView,
    updateTransactions
)

app_name='payments'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment_script/', PaymentView, name='payment'),
    path('charge/', charge, name='charge'), # new
    path('update-transactions/<subscription_id>/',updateTransactions,name='update-transactions'),
    # path('accounts/',include('django.contrib.auth.urls')),
    # path('accounts/signup/',SignupView.as_view,name='signup'),
    # path('accounts/signup/client/',ClientSignupView.as_view(),name='client_signup'),
    # path('accounts/signup/writer/',WriterSignupView.as_view(),name='writer_signup'),
    # path('accounts/signup/support/',SupportSignupView.as_view(),name='support_signup')
    # path('home/',PaymentIndexView,name='index')
    
]

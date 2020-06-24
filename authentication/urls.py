from django.urls import path
from .views import (
    UserLoginCreateView, 
    UserRegistrationCreateView,
    logout_view,
    ClientRegistrationCreateView,
    WriterRegistrationCreateView,
    show_notification,
    delete_notification,
    profile_view
)

app_name = 'authentication'

urlpatterns = [
    path('login', UserLoginCreateView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', UserRegistrationCreateView.as_view(), name='sign_up'),
    path('signup_client/', ClientRegistrationCreateView.as_view(), name='cient_sign_up'),
    path('signup_writer/', WriterRegistrationCreateView.as_view(), name='writer_sign_up'),
    path('notification/<int:notification_id>/',show_notification,name='show_notifications'),
    path('notification/delete/<int:notification_id>/',delete_notification,name='delete_notification'),
    path('profile/',profile_view,name='profile'),

]


#chat routing 
from django.urls import re_path

from .consumers import SupportToCustomerConsumer,SupportToWriterConsumer,NotificationsConsumer

websocket_urlpatterns=[
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$',SupportToCustomerConsumer),
    re_path(r'^ws/chat/writers/(?P<username>[\w.@+-]+)/$',SupportToWriterConsumer),
    re_path(r'^ws/notifications/$',NotificationsConsumer),
]
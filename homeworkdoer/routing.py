from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostOriginValidator,Orii
from django.urls import re_path,path
from django.conf.urls import url
import chat.routing
from chat.consumers import ChatConsumer,NotificationConsumer

application = ProtocolTypeRouter({
    'websocket' :AuthMiddlewareStack(
        URLRouter([
            url(r"^messages/(?P<username>[\w.@+-]+)/$",ChatConsumer),
            path("notifications/", NotificationConsumer),
        ])
    ),
})
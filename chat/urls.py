from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf.urls import url

from .views import ThreadView, InboxView,room,index,IndexView,ClientView,WriterView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view()),
    path("index/",index,name='index'),
    path('writers/',WriterView.as_view(),name='writer'),
    path('support/',ClientView.as_view(),name='client'),
    url(r'^index/', IndexView.as_view(template_name="search.html"),
                   name='chat_room'),
    re_path(r"^writers/(?P<username>[\w.@+-]+)", ThreadView.as_view(),name='threads'),
    re_path(r'^(?P<room_name>[^/]+)/$',room,name='room')
]


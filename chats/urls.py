from django.urls import path
from .views import Review,ReviewDetail,ChatBot,ChatRoom

app_name='chats'

urlpatterns = [
    # path('', ChatBot, name='chatbot'),
    # path('<str:room_name>/',ChatRoom, name='room'),
    path('chatty/home',Review,name='home'),
    path('detail/',ReviewDetail,name='detail'),
    
]

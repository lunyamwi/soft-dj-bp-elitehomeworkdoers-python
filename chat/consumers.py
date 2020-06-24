import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from .models import Thread,ChatMessage
from authentication.models import Notification

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        # await sleep(10)
        other_user=self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj=await self.get_thread(me,other_user)
        print(me,thread_obj.id)
        self.thread_obj=thread_obj
        chat_room=f"thread_{thread_obj.id}"
        self.chat_room=chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
             "type":"websocket.accept",
            #  "text":"Hello"
        })

    async def websocket_receive(self,event):
        print("receive",event)
        front_text=event.get('text',None)
        if front_text is not None:
            loaded_dict_data=json.loads(front_text)
            msg=loaded_dict_data.get('message')
            print(msg)
            user=self.scope['user']
            # username='default'
            # if user.is_authenticated:
            username=user.username
            myResponse={
                'message':msg,
                'username':username
            }
            await self.create_chat_message(user,msg)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":json.dumps(myResponse)
                }

            )
    
    # async def websocket_receive(self,event):
    #     print("receive", event)

    #     message_type = event.get('type', None)  #check message type, act accordingly
    #     if message_type == "notification_read":
    #          # Update the notification read status flag in Notification model.
    #          notification = Notification.object.get(id=notification_id)
    #          notification.notification_read = True
    #          notification.save()  #commit to DB
    #          print("notification read")

    #     front_text = event.get('text', None)
    #     if front_text is not None:
    #         loaded_dict_data = json.loads(front_text)
    #         msg =  loaded_dict_data.get('message')
    #         user = self.scope['user']
    #         username = 'default'
    #         if user.is_authenticated:
    #             username = user.username
    #         myResponse = {
    #             'message': msg,
    #             'username': username,
    #             'notification': notification_id  # send a unique identifier for the notification
    #         }
        
    
    async def chat_message(self,event):
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })
    
    async def websocket_disconnect(self,event):
        print("disconnected",event)
 
    @database_sync_to_async
    def get_thread(self,user,other_username):
        return Thread.objects.get_or_new(user,other_username)[0]

    @database_sync_to_async
    def create_chat_message(self,me,msg):
        thread_obj=self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg)




class NotificationConsumer(WebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            self.group_name=str(self.scope["user"].pk)
    
    async def disconnect(self,close_code):
        self.close()


    async def notify(self,event):
        self.send(text_data=json.dumps(event['text']))
        
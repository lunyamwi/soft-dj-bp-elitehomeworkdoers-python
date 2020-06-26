import asyncio
import json
from authentication.models import User,Notification
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage


class SupportToWriterConsumer(AsyncConsumer):
        '''
        this is a consumer for facilitating the 
        communication betwen the writers and the client
        '''
        async def websocket_connect(self,event):
            writer=self.scope['url_route']['kwargs']['username']
            support=self.scope['user']
            thread_obj=await self.get_thread(support,writer)
            self.thread_obj=thread_obj
            chat_room=f"thread_{thread_obj.id}"
            self.chat_room=chat_room
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
            await self.send({
                "type":"websocket.accept",
                "text":"hello"
            })

        async def websocket_receive(self,event):
            front_text=event.get('text',None)
            if front_text is not None:
                loaded_dict_data=json.loads(front_text)
                msg=loaded_dict_data.get('message')
                writer=self.scope['user']
                username=writer.username
                myResponse={
                    'message':msg,
                    'username':username
                }
                await self.create_chat_message(writer,msg)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type":"chat_message",
                        "text":json.dumps(myResponse)
                    }
                )

        async def chat_message(self,event):
            await self.send({
                "type":"websocket.send",
                "text":event['text']
            })

        async def websocket_disconnect(self,close_code):
            await self.channel_layer.group_discard(
                self.chat_room,
                self.channel_name
            )

        @database_sync_to_async
        def get_thread(self,support,writer):
            return Thread.objects.get_or_new(support,writer)[0]

        @database_sync_to_async
        def create_chat_message(self,support,msg):
            thread_obj=self.thread_obj
            return ChatMessage.objects.create(thread=thread_obj,user=support,message=msg)
        


class SupportToCustomerConsumer(WebsocketConsumer):
    '''
    in this consumer we want to ensure that a customer
    can directly chat with the support team without any issues
    '''
    def fetch_messages(self, data):
        messages = ChatMessage.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = ChatMessage.objects.create(
            user=author_user, 
            message=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.user.username,
            'content': message.message,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_support' 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))


class NotificationsConsumer(WebsocketConsumer):
    '''
    this consumer is for basically generating notifications so that
    it may send to the end users who are logged into the system. 
    e.g. 'you have a new message'
    '''
    async def connect(self):
        if  self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.group_name=str(self.scope['user'].pk)
        
    async def disconnect(self,close_code):
            await self.close()
    
    async def notify(self,event):
        self.send(text_data=json.dumps(event['text']))



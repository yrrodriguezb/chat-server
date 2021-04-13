import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.user_id = self.user.id
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.id

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # send message user connect
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connect', 
                'user_id': self.user_id,
                'user': self.user.username,
            }
        )

        # accept connection
        await self.accept()
    
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        now = timezone.now()

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # The event type
                'message': message, # The actual message you are sending
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def user_connect(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_disconnect(self, event):
        await self.send(text_data=json.dumps(event))

    # receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
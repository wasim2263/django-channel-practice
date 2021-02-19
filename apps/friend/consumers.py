# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class FriendConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user.username)
        if self.user == AnonymousUser():
            self.disconnect(404)
            return None
        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'] + " " + self.user.username

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

# chat/consumers.py
import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q, F

from apps.friend.models import Friend


class FriendConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user.username)
        if self.user == AnonymousUser():
            self.disconnect(404)
            return None
        Friend.objects.filter(user_1=self.user).update(user_1_connection_count=F('user_1_connection_count') + 1)
        Friend.objects.filter(user_2=self.user).update(user_2_connection_count=F('user_2_connection_count') + 1)
        friends = Friend.objects.filter(Q(user_1=self.user) | Q(user_2=self.user))
        for friend in friends:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                friend.connection_key,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_send)(
                friend.connection_key,
                {
                    'type': 'channel_message',
                    'message': friend.user_1.username + "+" + friend.user_2.username,
                    'status': 'connected'
                }
            )
        self.accept()

    def disconnect(self, close_code):

        Friend.objects.filter(user_1=self.user, user_1_connection_count__gt=0).update(
            user_1_connection_count=F('user_1_connection_count') - 1)
        Friend.objects.filter(user_2=self.user, user_2_connection_count__gt=0).update(
            user_2_connection_count=F('user_2_connection_count') - 1)

        friends = Friend.objects.filter(
            Q(user_1=self.user, user_1_connection_count=0) | Q(user_2=self.user, user_2_connection_count=0))
        # .distinct('id')
        for friend in friends:
            # leave room group
            self.channel_layer.group_discard(
                friend.connection_key,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_send)(
                friend.connection_key,
                {
                    'type': 'channel_message',
                    'message': friend.user_1.username + "+" + friend.user_2.username,
                    'status': 'disconnected'
                }
            )

    def channel_message(self, event):
        message = event['message']
        status = event['status']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'status': status
        }))

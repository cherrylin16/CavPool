import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
        me = self.scope["user"]
        self.room_name = f"chat_{min(me.id, self.other_user_id)}_{max(me.id, self.other_user_id)}"
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        sender = self.scope["user"]
        receiver = await self.get_user(self.other_user_id)

        msg = await self.create_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender": sender.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
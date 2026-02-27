import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Ensure room exists
        await self.get_or_create_room()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send latest messages
        messages = await self.get_last_messages()
        history = [
            {"message": msg.content, "username": msg.user.username}
            for msg in messages
        ]

        await self.send(text_data=json.dumps({
            "history": history
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Save to DB
        message = await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message.content, "username": self.scope["user"].username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": event["username"],}))

    # ===== Database Helpers =====

    @sync_to_async
    def get_or_create_room(self):
        return Room.objects.get_or_create(name=self.room_name)

    @sync_to_async
    def save_message(self, message_text):
        room = Room.objects.get(name=self.room_name)
        user = User.objects.get(pk=self.scope['user'].id)
        return Message.objects.create(room=room, user=user, content=message_text)

    @sync_to_async
    def get_last_messages(self):
        return list(
            Message.objects.filter(room__name=self.room_name)
            .select_related("user")
            .order_by("timestamp")[:50]
        )

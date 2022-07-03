"""In this file, we define the consumers for the chat application."""

# Importing libraries
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatModel

class PersonalChatConsumer(AsyncWebsocketConsumer):
    """This class defines the consumer for personal chat."""

    async def connect(self):
        """Connect the user to the chat."""
        my_id = self.scope['user'].id

        # kwargs: get the id from websocket url
        other_user_id = self.scope['url_route']['kwargs']['id']

        # Creating a unique group name for the chat
        if int(my_id) > int(other_user_id):
            self.room_name = f"{my_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{my_id}"

        self.room_group_name = "chat_%s" % self.room_name

        # fmt: off
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name,)

        await self.accept()
        await self.send(text_data=self.room_group_name)

    async def disconnect(self, code):
        """Disconnect the user from the chat."""
        self.channel_layer.group_discard(self.room_group_name,
                                         self.channel_layer)

    async def receive(self, text_data=None, bytes_data=None):
        """Receive the message from the user."""
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )
        
    async def chat_message(self, event):
        """Send the message to the user."""
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
        
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.event_handlers import event_handlers


class ChatConsumer(AsyncWebsocketConsumer):

    event_handlers = {
        **event_handlers
    }

    def get_group_name(self):
        return self.user.username if self.user else 'Guest'

    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.get_group_name(),
            self.channel_name
        )
        await self.accept()
        
        if (self.user):
            await self.event_handlers['initial_message'].handle(self)
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.get_group_name(),
            self.channel_name
        )

    async def receive(self, text_data):
        if not self.user:
            await self.send_error("unAuthenticated, closing the connection...")
            return await self.close()

        data = json.loads(text_data)
        event_type = data.get('type')
        if event_type in self.event_handlers:
            await self.event_handlers[event_type].handle(self, data)
        else:
            await self.send_error("Invalid event type")

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['message']['type'],
            'message': event['message'],
        }))
        
    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message,
        }))

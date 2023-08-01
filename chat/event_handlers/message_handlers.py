from chat.database_utils import DatabaseUtils
from chat.event_handlers.base_handlers import BaseEventHandler


class MessageHandler(BaseEventHandler):
    async def create_message(self, user,  data):
        return await DatabaseUtils.create_message(
        content=data.get('content', None),
        sender=user.id,
        chat_room=data.get('group_id', None)
        )
    
    async def handle(self, data, message):
        raise NotImplementedError(
            "handle method must be implemented in subclass")

class GroupChatHandler(MessageHandler):
    async def handle(self, consumer, data):
        # check group_id
        message = await self.create_message(consumer.user, data)
        
        group_users = await DatabaseUtils.fetch_group_users(
            data.get('group_id')
        )

        for user in group_users:

            await consumer.channel_layer.group_send(
                user.username,
                {
                    'type': 'send_message',
                    'message': {'message': message, 'type': 'group_message'},
                },
            )
        


class PrivateMessageHandler(MessageHandler):
    async def handle(self, consumer, data):
        self.create_message(data, message)
        

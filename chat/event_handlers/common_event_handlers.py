import json
from chat.event_handlers.base_handlers import BaseEventHandler
from chat.database_utils import DatabaseUtils


class InitialMessageHandler(BaseEventHandler):
    async def handle(self, consumer):
        await consumer.send(
            text_data=json.dumps({
                'type': 'user',
                'message': await DatabaseUtils.fetch_user(consumer.user.id)
            })
        )

        await consumer.send(
            text_data=json.dumps({
                'type': 'user_group',
                'message': await DatabaseUtils.get_paginated_chats(consumer.user, 1, 20)
            })
        )


class FetchGroupMessages(BaseEventHandler):
    async def handle(self, consumer, data):
        await consumer.send(
            text_data=json.dumps({
                'type': 'group_messages',
                'message': {
                    'messages': await DatabaseUtils.fetch_group_messages(data.get('group_id')),
                    'group_id': data.get('group_id'),
                },
            })
        )

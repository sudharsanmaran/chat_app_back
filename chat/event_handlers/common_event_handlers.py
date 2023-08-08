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
        return


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
        return


class searchUsers(BaseEventHandler):
    async def handle(self, consumer, data):
        await consumer.send(
            text_data=json.dumps({
                'type': 'search_users',
                'message': {
                    'result': await DatabaseUtils.search_users(data.get('search_query')),
                },
            })
        )
        return
    
class CreatePrivateChatRoomHandler(BaseEventHandler):
    async def handle(self, consumer, data):
        await consumer.send(
            text_data=json.dumps({
                'type': 'new_group',
                'message':  await DatabaseUtils.create_private_chat_room(users=data.get('users')),
            })
        )
        return
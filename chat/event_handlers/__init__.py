from chat.event_handlers.common_event_handlers import (
    CreatePrivateChatRoomHandler, FetchGroupMessages,
    InitialMessageHandler, searchUsers
)
from chat.event_handlers.message_handlers import GroupChatHandler, PrivateMessageHandler


event_handlers = {
    'initial_message': InitialMessageHandler(),
    'fetch_group_messages': FetchGroupMessages(),
    'group_message': GroupChatHandler(),
    'private_message': PrivateMessageHandler(),
    'search_users': searchUsers(),
    'create_private_chat_room': CreatePrivateChatRoomHandler()
}

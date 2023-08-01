from chat.event_handlers.common_event_handlers import FetchGroupMessages, InitialMessageHandler
from chat.event_handlers.message_handlers import GroupChatHandler, PrivateMessageHandler


event_handlers = {
    'initial_message': InitialMessageHandler(),
    'fetch_group_messages': FetchGroupMessages(),
    'group_message': GroupChatHandler(),
    'private_message': PrivateMessageHandler(),
}

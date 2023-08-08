from datetime import datetime, timezone
from channels.db import database_sync_to_async
from chat.models import ChatRoom, User, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer, UserSerializer
from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.core.paginator import Paginator
from django.db.models import Max

PRIVATE_MAX_USER_COUNT = 2
GROUP_MAX_USER_COUNT = 20
PRIVATE_CHAT_ROOM_NAME = "Private Room"


def get_private_room_name(users):
    return ''.join(str(user.get('id')) for user in users)


class ChatRoomUtils:

    @staticmethod
    @database_sync_to_async
    def fetch_group_users(group_id):
        group = ChatRoom.objects.prefetch_related('users').get(pk=group_id)
        return group.users.all()

    @staticmethod
    @database_sync_to_async
    def get_paginated_chats(user, page_number, items_per_page):

        group_chats = list(ChatRoom.objects.filter(users=user).annotate(
            last_message_time=Max('messages__created_at')
        ))

        sorted_chats = sorted(
            group_chats, key=lambda chat: chat.updated_at, reverse=True)

        paginator = Paginator(sorted_chats, items_per_page)
        current_page = paginator.get_page(page_number)

        return ChatRoomSerializer(current_page, many=True).data

    # @staticmethod
    # @database_sync_to_async
    # def create_group_chat_room(name, users, is_private=False):
    #     pass

    @staticmethod
    @database_sync_to_async
    def create_private_chat_room(users):
        new_private_chat_room = ChatRoom.objects.create_private_chat_room(
            name=get_private_room_name(users), users=users)
        return ChatRoomSerializer(new_private_chat_room).data


class UserUtils:

    @staticmethod
    @database_sync_to_async
    def fetch_user(user_id):
        try:
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, CoreValidationError):
            return
        return UserSerializer(user).data

    @staticmethod
    @database_sync_to_async
    def search_users(query: str):
        users = User.search_by_username(query)
        return UserSerializer(users, many=True).data


class MessageUtils:

    @staticmethod
    @database_sync_to_async
    def create_message(**kwargs):
        serializer = MessageSerializer(data={**kwargs})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return
        else:
            message = serializer.save()
            chat_room = message.chat_room
            chat_room.updated_at = datetime.now(timezone.utc)
            chat_room.save()
            return serializer.data

    @staticmethod
    @database_sync_to_async
    def fetch_group_messages(group_id):
        messages = list(Message.objects.filter(chat_room=group_id))[::-1]
        return MessageSerializer(messages, many=True).data


class DatabaseUtils(ChatRoomUtils, UserUtils, MessageUtils):
    pass

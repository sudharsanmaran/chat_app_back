from datetime import datetime, timezone
from channels.db import database_sync_to_async
from chat.models import ChatRoom, User, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer, UserSerializer
from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.core.paginator import Paginator
from django.db.models import Max

class DatabaseUtils:

    @staticmethod
    @database_sync_to_async
    def fetch_group_users(group_id):
        group = ChatRoom.objects.prefetch_related('users').get(pk=group_id)
        return group.users.all()
    
    @staticmethod
    @database_sync_to_async
    def fetch_user_groups(user_id):
        group = ChatRoom.objects.prefetch_related('users').get(pk=user_id)
        return group.users.all()

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
    def create_message(**kwargs):
        serializer = MessageSerializer(data={**kwargs})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return
        else:
            message = serializer.save()
            # Get the associated ChatRoom for this message
            chat_room = message.chat_room

            # Update the `updated_at` field of the associated ChatRoom
            chat_room.updated_at = datetime.now(timezone.utc)
            chat_room.save()
            return serializer.data
        
    @staticmethod
    @database_sync_to_async
    def get_paginated_chats(user, page_number, items_per_page):

        group_chats = list(ChatRoom.objects.filter(users=user).annotate(
            last_message_time=Max('messages__created_at')
        ))

        sorted_chats = sorted(group_chats, key=lambda chat: chat.updated_at, reverse = True)

        paginator = Paginator(sorted_chats, items_per_page)
        current_page = paginator.get_page(page_number)
        
        return ChatRoomSerializer(current_page, many=True).data
    
    @staticmethod
    @database_sync_to_async
    def fetch_group_messages(group_id):
        messages = list(Message.objects.filter(chat_room=group_id))[::-1]
        return MessageSerializer(messages, many=True).data

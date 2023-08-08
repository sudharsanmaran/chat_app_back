from rest_framework import serializers
from chat.models import Message, ChatRoom, User


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['last_login', 'groups',
                            'user_permissions', 'is_staff', 'is_superuser']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ['last_login', 'groups',
                            'user_permissions', 'is_staff', 'is_superuser']


class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = ChatRoom
        fields = '__all__'
        
    # def get_users(self, obj):
    #     return [str(uuid) for uuid in obj.users.values_list('id', flat=True)]


class MessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.UUIDField(source='chat_room.id',required=False, allow_null=True)
    sender = serializers.UUIDField(source='sender.id')

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        chat_room_id = validated_data.pop('chat_room')['id']
        sender_id = validated_data.pop('sender')['id']
        chat_room = None
        
        if chat_room_id:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender = User.objects.get(id=sender_id)

        return Message.objects.create(
            chat_room=chat_room,
            sender=sender,
            **validated_data
        )

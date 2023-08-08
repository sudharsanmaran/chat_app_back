from rest_framework import generics, permissions
from chat.models import ChatRoom, User, Message
from chat.serializers import ChatRoomSerializer, UserSerializer, MessageSerializer, UserRequestSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status


@extend_schema(
    tags=['ChatRooms'],
)
class ListChatRoomAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(users=self.request.user)


# @extend_schema(
#     tags=['ChatRooms'],
# )
# class CRUDChatRoomAPIView(generics):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ChatRoomSerializer

#     def get_queryset(self):
#         return ChatRoom.objects.filter(users=self.request.user)

@extend_schema(
    tags=['ChatRoom\'s Messages'],
)
class ListMessagesAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_room_id = self.kwargs['chat_room_id']
        return Message.objects.filter(
            chat_room=chat_room_id
        )



@extend_schema(
    tags=['User Details'],
    responses=UserSerializer
)
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserRequestSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return UserCreateView._perform_create(serializer)

    @staticmethod
    def _perform_create(serializer):
        validated_data = {**serializer.validated_data}
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        return User.objects.create_or_update_user(
            username=username,
            password=password,
            **validated_data
        )


@extend_schema(
    tags=['Users List'],
)
class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(
    tags=['User Details'],
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        return UserCreateView._perform_create(serializer)

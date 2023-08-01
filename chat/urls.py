from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from chat.views import ListChatRoomAPIView, UserDetailView, UserListView, UserCreateView, ListMessagesAPIView


app_name = 'chat'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/chat_rooms/', ListChatRoomAPIView.as_view(), name='groups'),
    path('api/user/register/', UserCreateView.as_view(), name='user_create'),
    path('api/user_list/', UserListView.as_view(), name='users_list'),
    path('api/user/', UserDetailView.as_view(), name='user_details'),
    path('api/messages/<uuid:chat_room_id>',
         ListMessagesAPIView.as_view(), name='group_messages'),
]

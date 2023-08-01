from rest_framework.response import Response
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from jwt import InvalidTokenError, decode as jwt_decode, DecodeError
from rest_framework_simplejwt.tokens import UntypedToken, TokenError
from chat.serializers import UserSerializer
from . import settings

User = get_user_model()
 
 
@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
   
    except User.DoesNotExist:
        return None
    
class UnauthenticatedWebsocketConnection(Exception):
    pass
 
 
class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        query_string = scope['query_string']
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict.get("token", [None])[0]
        # print("Token", token, jwt_decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]))

        try:
            decoded_data = jwt_decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(decoded_data['user_id'])
            scope["user"] = user
        except DecodeError:
             scope["user"] = None
        print(scope, 'scope')
        return await self.app(scope, receive, send)
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode, DecodeError
from . import settings

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)

    except User.DoesNotExist:
        return None


@database_sync_to_async
def login(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        pass
    return None


class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string']
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict.get("token", [None])[0]
        scope["user"] = None
        if not token:
            username = query_dict.get("username", [None])[0]
            password = query_dict.get("password", [None])[0]
            if username and password:
                user = await login(username, password)
                if user:
                    scope["user"] = user
        else:
            try:
                decoded_data = jwt_decode(
                    jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(decoded_data['user_id'])
                scope["user"] = user
            except DecodeError as e:
                print(e)

        return await self.app(scope, receive, send)

import jwt
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get('headers'))

        if b'authorization' in headers:
            try:
                token = headers[b'authorization'].decode().split(' ')[1]
                decoded = jwt.decode(token, options={"verify_signature": False})
                scope['user'] = await self.get_user(decoded['user_id'])
            except Exception as e:
                print(e)
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return settings.AUTH_USER_MODEL.objects.get(id=user_id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            return AnonymousUser()
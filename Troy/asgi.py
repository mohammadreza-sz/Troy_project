# you can delete this file...


# import os

# from django.core.asgi import get_asgi_application

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Troy.settings')

# # application = get_asgi_application()
# django_asgi_app = get_asgi_application()
# import chat.routing

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
#         ),
#     }
# )
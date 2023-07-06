# import os

# from django.core.asgi import get_asgi_application

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from Troy.middleware import JwtAuthMiddleware

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Troy.settings')
# import django
# django.setup()

# # application = get_asgi_application()
# django_asgi_app = get_asgi_application()
# import chat.routing

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket":AuthMiddlewareStack(
#             URLRouter(chat.routing.websocket_urlpatterns))
#         ,
#         # 'websocket': JwtAuthMiddleware(
#         #     URLRouter(
#         #         [
#         #             path('ws/some_path/', consumers.MyConsumer.as_asgi()),
#         #         ]
#         #     )
#         # ),
#     }
# )
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Troy.settings')

import django
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from invoice.routing import websocket_urlpatterns
import chat.routing


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)

        # URLRouter(
        #     chat.routing.websocket_urlpatterns
        # )
    ),
})
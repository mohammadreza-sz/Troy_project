from django.urls import re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    # re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    re_path(r'chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),

]
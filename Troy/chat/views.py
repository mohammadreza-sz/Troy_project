from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer

# User = get_user_model()

# def get_last_30_messages(chatId):
#     chat = get_object_or_404(Chat, id = chatId)
#     return chat.messages.order_by('_timestamp').all()[:30]

# def get_user_contact(username):
#     user = get_object_or_404(User, username = username)
#     return get_object_or_404(Contact, user = user)

# def get_current_chat(chatId):
#     return get_object_or_404(Chat, id = chatId)

# from django.contrib.auth.decorators import login_required

# # from chat.models import Room, Message
# from django.utils.safestring import mark_safe
# import json
# from django.http import HttpResponse, JsonResponse

# # def home(request):
# #     return render(request, 'home.html')

# def index(request):
#     return render(request, 'chat/index.html', {})

# @login_required
# def room(request, room_name):
#     return render(request, "chat/room.html", {
#         "room_name_json": mark_safe(json.dumps(room_name)),
#         "username" : mark_safe(json.dumps(request.user.username)),
#     })



class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = IsAuthenticated

    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'index',
        url_name='chat_index',
        permission_classes=[AllowAny]
    )
    def index(self, request):

        return render(request, 'chat/index.html')

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path=r'room/(?P<room_name>\w+)/username/(?P<username>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def room(self, request, room_name, username):

        messages = Chat.objects.filter(room=room_name)

        return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})
    
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'room/messages/(?P<room_name>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def get_room_messages(self, request, room_name, *args, **kwargs):
        
        try:
            chats = Chat.objects.filter(room_name=room_name)
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


def room(request, room_name, username):
    messages = Chat.objects.filter(room_name=room_name)
    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})
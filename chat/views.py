from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Chat, Contact

User = get_user_model()

def get_last_30_messages(chatId):
    chat = get_object_or_404(Chat, id = chatId)
    return chat.messages.order_by('_timestamp').all()[:30]

def get_user_contact(username):
    user = get_object_or_404(User, username = username)
    return get_object_or_404(Contact, user = user)

def get_current_chat(chatId):
    return get_object_or_404(Chat, id = chatId)

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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# def home(request):
#     return render(request, 'home.html')

def index(request):
    return render(request, "chat/index.html")

@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name_json": mark_safe(json.dumps(room_name)),
        "username" : mark_safe(json.dumps(request.user.username)),
    })
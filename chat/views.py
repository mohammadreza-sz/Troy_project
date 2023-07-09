from django.shortcuts import render, redirect
# from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from .serializer import CustomChatSerializer
from rest_framework.response import Response
from .models import Conversation
from rest_framework import status

# def home(request):
#     return render(request, 'home.html')

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class CustomChat(APIView):
    def get(self , request):
        room_name = Conversation.objects.all()
        serializer = CustomChatSerializer(room_name , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
from dataclasses import fields

from itertools import count

from re import search

from rest_framework import serializers

from .models import *

from django.conf import settings

class CustomChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields  =['room_name']
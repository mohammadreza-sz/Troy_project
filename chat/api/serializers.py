from rest_framework import serializers

from chat.models import Chat

# we must modify it..

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        friends = ('__all__')
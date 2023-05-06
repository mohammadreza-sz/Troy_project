import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Chat, Contact
from .view import get_last_30_messages, get_user_contact, get_current_chat

User = get_user_model()

# helen changes Async to async_to_sync
class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # print(data)
        messages = get_last_30_messages(data['chatId'])
        # print(messages)
        content = {
            'cammand' : 'messages',
            'messages' : self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        # author_user = Uesr.objects.filter(username = author)[0]
        message = Message.objects.create(
            contact = user_contact, 
            content = data['message'])
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.messages_to_json(messages))
        return result

    def message_to_json(self, message):
        return {
            'id' : message.id,
            'author': message.contact.user.username,
            'content' : message.content,
            'timestamp' : str(message.timestamp)
        }

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message':new_message
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        # user = self.scope["user"]        
        # if user.username != "mrs2":
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
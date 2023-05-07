import json
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Chat
from Troy.settings import AUTH_USER_MODEL
# from .view import get_last_30_messages, get_user_contact, get_current_chat
User = AUTH_USER_MODEL

# helen changes Async to async_to_sync
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
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
        message = data['message']
        username = data['username']
        room = data['room_name']
        sender_type = data['sender_type']

        user = User.objects.get(username = username)
        # self.commands[data['command']](self, data)/
        # async_to_sync(self.save_mesa)

        async_to_sync(self.save_message)(user, room, message, sender_type)

            # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'sender_type':sender_type
            }
        )

    def chat_message(self, event):
        message = event["message"]
        username = event['username']
        sender_type = event['sender_type']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sender_type':sender_type
        }))


    @sync_to_async
    def save_message(self, user, room, message, sender_type):
        Chat.objects.create(sender=user, room_name=room, message=message, sender_type=sender_type)
    
    
    # def fetch_messages(self, data):
    #     # print(data)
    #     messages = get_last_30_messages(data['chatId'])
    #     # print(messages)
    #     content = {
    #         'cammand' : 'messages',
    #         'messages' : self.messages_to_json(messages)
    #     }
    #     self.send_message(content)

    # def new_message(self, data):
    #     user_contact = get_user_contact(data['from'])
    #     # author_user = Uesr.objects.filter(username = author)[0]
    #     message = Message.objects.create(
    #         contact = user_contact, 
    #         content = data['message'])
    #     current_chat = get_current_chat(data['chatId'])
    #     current_chat.messages.add(message)
    #     current_chat.save()
    #     content = {
    #         'command' : 'new_message',
    #         'message' : self.message_to_json(message)
    #     }
    #     return self.send_chat_message(content)

    # def messages_to_json(self, messages):
    #     result = []
    #     for message in messages:
    #         result.append(self.messages_to_json(messages))
    #     return result

    # def message_to_json(self, message):
    #     return {
    #         'id' : message.id,
    #         'author': message.contact.user.username,
    #         'content' : message.content,
    #         'timestamp' : str(message.timestamp)
    #     }

    # commands = {
    #     'fetch_messages' : fetch_messages,
    #     'new_message':new_message
    # }



    # def send_chat_message(self, message):
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, 
    #         {
    #             "type": "chat_message", 
    #             "message": message
    #         }
    #     )

    # def send_message(self, message):
    #     self.send(text_data=json.dumps(message))

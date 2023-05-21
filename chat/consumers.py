# import json

# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))

# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))

import json

from channels.generic.websocket import AsyncWebsocketConsumer , AsyncJsonWebsocketConsumer
from .models import Conversation , Message
from jwt.exceptions import InvalidTokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from account.models import User as UserModel
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room_group_name = "chat_%s" % self.room_name

        # # Join room group
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # user = self.scope["user"]        
        # if user.username != "mrs2":
        #     await self.accept()

        # if not self.scope["user"].is_authenticated:        
        #     await self.send_json({'error': 'User is not authenticated'})            
        #     await self.close()
    # commands = {
    #     'fetch_messages': fetch_messages,
    #     'new_message': new_message
    # }

    # def fetch_messages(self, data):
    #     room_id = data['room_id']
    #     room = Room.objects.get(room_id=room_id)
    #     message = Message(room_id=room)
    #     messages = message.last_30_messages(message)
    #     content = {
    #         'command': 'fetch-messages',
    #         'messages': self.messages_to_json(messages)
    #     }
    #     self.send_message(content)
    async def connect(self):
        # Get the JWT token from the request headers
            # token = self.scope['headers'][b'authorization'][0].decode('utf-8').split(' ')[1]
            # t = "fjksl"
        index = self.get_index_of_jwt_token()
        if index != -1:                            
            token = self.scope['headers'][index][1].decode('utf-8').split(' ')[1]
        else:
            # await self.websocket.close(code=1000)
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "chat_%s" % self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()            
            await self.close()
            # await self.send({"type": "websocket.close", "code": 1009})
            return
            print("user is anonymose")
            
        try:
            # Verify and decode the JWT token
            validated_token = self.jwt_decode(token)
            
            # Get the user ID from the decoded token
            user_id = validated_token['user_id']
            
            # Authenticate the user using Django's built-in authentication backend
            user = await self.get_user(user_id)
            # user = User.objects.get(id =user_id)
                # conversation = Conversation.objects.get(id=self.room_name)

            # If the user is authenticated, accept the WebSocket connection
            if user.is_authenticated:
                self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
                self.room_group_name = "chat_%s" % self.room_name
                self.scope['user'] = user
                # Join room group
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                print("\n\n\n"+user.first_name)
                await self.accept()
                # conversation =await self.get_conversation(self.room_name)# Conversation.objects.get(room_name=self.room_name)#################************************
                # if conversation is None:
                #     message =await self.last_message(conversation)
                #     await self.send_json(message)

            else:
                await self.send_json({'error': 'User is not authenticated'})            
                await self.close()
        except (InvalidTokenError, InvalidToken):
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "chat_%s" % self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.close()
                
                
    def get_index_of_jwt_token(self):
        length = len(self.scope['headers'])
        index = -1
        for i in range (length) :
            if self.scope['headers'][i][0] == b'authorization' :
                index = i
                break
        return index
        
    def jwt_decode(self, token):
        """
        Decode and validate a JWT token.
        """
        from django.conf import settings
        from rest_framework_simplejwt.tokens import AccessToken
        
        try:
            return AccessToken(token).payload
        except Exception as e:
            raise InvalidToken(e)
    
        

    async def disconnect(self, code):
        # print(code)
        # Leave room group
        # if close_code == 1009:
            # pass
            # await self.close()
        # else:
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
         # Save message to database
        # conversation = Conversation.objects.get(room_name=self.room_name)#################************************
        # conversation =await self.get_conversation(self.room_name)# Conversation.objects.get(room_name=self.room_name)#################************************
        
        # sender = self.scope['user']
        # receiver = conversation.participants.exclude(id=sender.id).first()
        # receiver = await self.get_receiver(sender.id)

        # new_message = Message(sender=sender, receiver=receiver, text=message, conversation=conversation)
        # new_message.save()
        # await self.create_message(sender , receiver , conversation , message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
            # self.room_group_name, {"type": "chat_message2", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message }))#,"username": username}))
    
    @database_sync_to_async
    def last_message(self , conversationn):
        return  Conversation.objects.order_by('-timestamp').filter(conversation = conversationn)[:2]
    @database_sync_to_async
    def create_message(self , sender , receiver , conversation , message):
        new_message = Message(sender=sender, receiver=receiver, text=message, conversation=conversation)
        new_message.save()

    @database_sync_to_async
    def get_conversation(self, room_namee):
        try:
            return Conversation.objects.filter(room_name=room_namee)
        except UserModel.DoesNotExist:
            return None
        # return 
    @database_sync_to_async
    def get_receiver(self ,sender_id):
        return Conversation.participants.exclude(id=sender_id).first()

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Get the user object for the given user ID.
        """
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        #     return AnonymousUser()
        # from django.contrib.auth import get_user_model
        
        # # User = get_user_model()
        # User = UserModel.objects.get(id =user_id)

        # try:
        #     return await self.scope['django'].get_or_connect(User, id=user_id)
        # except User.DoesNotExist:
            # return None

#####************************************************************************************




# from channels.consumer import SyncConsumer

# class EchoConsumer(SyncConsumer):

#     def websocket_connect(self, event):
#         self.send({
#             "type": "websocket.accept",
#         })

#     def websocket_receive(self, event):
#         self.send({
#             "type": "websocket.send",
#             "text": event["text"],
#         })
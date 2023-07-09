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
from .models import Connection, Conversation , Message
from jwt.exceptions import InvalidTokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from account.models import User as UserModel
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json



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
        #region authentication 
        # index = self.get_index_of_jwt_token()
        # if index != -1:                     
        #     token = self.scope['headers'][index][1].decode('utf-8').split(' ')[1]
        # else:#if user not login or front doesn't pass authorization header
        #     # await self.websocket.close(code=1000)
        #     self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #     self.room_group_name = "chat_%s" % self.room_name
        #     await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #     await self.accept()            
        #     await self.send_json({'error': 'User is not authenticated'})
        #     await self.close()
        #     # await self.send({"type": "websocket.close", "code": 1009})
        #     return
        #     print("user is anonymose")
            
        # try:
        #     # Verify and decode the JWT token
        #     validated_token = self.jwt_decode(token)
            
        #     # Get the user ID from the decoded token
        #     user_id = validated_token['user_id']
            
        #     # Authenticate the user using Django's built-in authentication backend
        #     user = await self.get_user(user_id)
        #     # user = User.objects.get(id =user_id)
        #         # conversation = Conversation.objects.get(id=self.room_name)

        #     # If the user is authenticated, accept the WebSocket connection
        #     if user.is_authenticated:
        #         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #         self.room_group_name = "chat_%s" % self.room_name
        #         self.scope['user'] = user
        #         # Join room group
        #         # if channle count more than two must diconnected********************************
        #         # await check_duplicat_room()
        #         await self.channel_layer.group_add(self.room_group_name, self.channel_name)#group is collection of channels
        #         # print("\n\n\n"+user.first_name)
        #         await self.accept()
        #         await self.user_on({'user':user,'status':True})
        #         conversation =await self.get_conversation(self.room_name)# Conversation.objects.get(room_name=self.room_name)#################************************
        #         if conversation is not None:
        #             message =await self.last_message(conversation)#perhaps doesn't return anything here but no matter
        #             for m in message:
        #                 await self.receive(json.dumps({"fetch_message":m.text}))
        #             # await self.send_json(message)
        #         else:
        #             await self.create_conversation(self.room_name)

        #     else:
        #         await self.send_json({'error': 'User is not authenticated'})            
        #         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #         self.room_group_name = "chat_%s" % self.room_name
        #         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #         await self.accept()
        #         await self.close()
        # except (InvalidTokenError, InvalidToken):
        #     await self.send_json({'error': 'User is not authenticated'})            
        #     self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #     self.room_group_name = "chat_%s" % self.room_name
        #     await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #     await self.accept()
        #     await self.close()
        #endregion   
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # self.scope['user'] = user******because remove authentication
        # Join room group
        # if channle count more than two must diconnected********************************
        # await check_duplicat_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)#group is collection of channels
        # print("\n\n\n"+user.first_name)
        await self.accept()
        # await self.user_on({'user':user,'status':True})******because remove authentication
        conversation =await self.get_conversation(self.room_name)# Conversation.objects.get(room_name=self.room_name)#################************************
        if conversation is not None:
            message =await self.last_message(conversation)#perhaps doesn't return anything here but no matter
            for m in message:
                await self.receive(json.dumps({"fetch_message":m.text}))
            # await self.send_json(message)
        else:
            await self.create_conversation(self.room_name)
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
        # await self.user_off(self.scope['user']) ******because remove authentication
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))

    def set_variable(self, value):
        setattr(self.__class__, 'new_variable', value)
    # Receive message from WebSocket
    async def receive(self, text_data:dict):
        text_data_json = json.loads(text_data)
        if "receiver_id" in text_data_json:
            print ("\n\n\n\n\n receiver_id :" , text_data_json["receiver_id"])
            async_to_sync( setattr(self.__class__, 'receiver_id', text_data_json["receiver_id"]))
            async_to_sync( setattr(self.__class__, 'sender_id', text_data_json["sender_id"]))
            # await self.set_variable( text_data_json["receiver_id"])
            print("\nnew variable set\n")

            # messages = message.last_30_messages(message)
            # content = {
            # # 'command': 'fetch-messages',
            # 'messages': await self.messages_to_json(messages)
            # }
            # self.send_message(content)
            # print("\n\n\n\n\n" , content)
        elif "fetch_message" in text_data_json:
            message = text_data_json["fetch_message"]
            # await self.channel_layer.group_send(
            #     self.room_group_name, {"type": "chat_message", "message": message}
            #     # self.room_group_name, {"type": "chat_message2", "message": message}
            # )
            await self.channel_layer.send(self.channel_name, {
                "type": "send_to_single_channel",
                "message": message,
})
        else:
            message = text_data_json["message"]
            # Save message to database
            # conversation = Conversation.objects.get(room_name=self.room_name)#################************************
            conversation =await self.get_conversation(self.room_name)# Conversation.objects.get(room_name=self.room_name)#################************************
            
            # sender = self.scope['user']******because remove authentication
            # sender_id = text_data_json["sender_id"]
            sender = await self.get_sender(self.sender_id)
            # receiver = conversation.participants.exclude(id=sender.id).first()
            receiver = await self.get_user(self.receiver_id)

            # new_message = Message(sender=sender, receiver=receiver, text=message, conversation=conversation)
            # new_message.save()
            await self.create_message(sender , receiver , conversation , message)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "send_to_all_channels", "message": message}
                # self.room_group_name, {"type": "chat_message2", "message": message}
            )
        return 

    # Receive message from room group
    async def send_to_all_channels(self, event):
        message = event["message"]
        # username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message }))#,"username": username}))
    async def send_to_single_channel(self ,event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message }))#,"username": username}))
        # pass
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
        
    @database_sync_to_async
    def user_off(self , user):
        obj = Connection.objects.get(user = user)
        obj.status=False
        obj.save()
    @database_sync_to_async
    def user_on(self , data):
        obj, created = Connection.objects.get_or_create(
        user=data['user'],
        # field2=data['status']
    )
        obj.status = data['status']
        obj.save()
        # return obj


    @database_sync_to_async
    def create_conversation(self, room_namee):
        new_conversation = Conversation(room_name = room_namee)
        new_conversation.save()
    @database_sync_to_async
    def last_message(self , conversationn):
        qs=  Message.objects.order_by('timestamp').filter(conversation = conversationn).all()
        # for mess in qs.values('room_name'):
        #     print(mess.room_name , "\n\n\n")
        #     # people_list.append(person_obj)
        # for message in m:
        #     self.receive({"message":message.text})
        return list(qs)
    @database_sync_to_async
    def create_message(self , sender , receiver , conversation , message):
        new_message = Message(sender=sender, receiver=receiver, text=message, conversation=conversation)
        new_message.save()

    @database_sync_to_async
    def get_conversation(self, room_namee):
        try:
            return Conversation.objects.filter(room_name=room_namee).first()
        except UserModel.DoesNotExist:
            return None
        # return 
    @database_sync_to_async
    def get_receiver(self ,sender_id):
        return Conversation.participants.exclude(id=sender_id).first()
        # return 

    @database_sync_to_async
    def get_sender(self,sender_id):
        try:
            return UserModel.objects.get(id = sender_id)
        except UserModel.DoesNotExist:
            return None
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
from django.shortcuts import render
from rest_framework.views import APIView #heln
from rest_framework.generics import GenericAPIView #helen
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from djoser import signals
from djoser.compat import get_user_email
# from .serializers import ActivationSerializer
from rest_framework.generics import GenericAPIView
import requests
from pprint import pprint

#helen{ 
from django.http import HttpResponseBadRequest, HttpResponse
class BadRequestException(Exception):

    def __init__(self, message='', *args, **kwargs):

        self.message = message

def my_view(request):

    try:
        data = get_data_from_another_func()
    except BadRequestException as e:
        return HttpResponseBadRequest(e.message)
    process_data(data)

    return HttpResponse('Thank you')

def get_data_from_another_func():
    raise BadRequestException(message='something wrong')
def process_data(data):
    pass

#}helen

#mrs

# @api_view(['post'] )

# def activation(self, request, uid , token, *args, **kwargs ):

#     # def get_serializer_context(self):#lesson 22

#     #     return {'uid':uid , 'token':token}



#     # serializer = self.get_serializer(data=request.data ,context= {'uid':uid , 'token':token})

#     serializer = ActivationSerializer(data=request.data ,context= {'uid':uid , 'token':token})

#     # serializer = ActivationSerializer(data={"uid":uid , "token":token} ,context= {'uid':uid , 'token':token})

#     pprint("\n \n \n \n")

#     pprint(serializer.initial_data) # this will print {'foo':'bar'}



#     serializer.is_valid(raise_exception=True)

#     user = serializer.user

#     user.is_active = True

#     user.save()



#     signals.user_activated.send(

#         sender=self.__class__, user=user, request=self.request

#     )



#     if settings.SEND_CONFIRMATION_EMAIL:

#         context = {"user": user}

#         to = [get_user_email(user)]

#         settings.EMAIL.confirmation(self.request, context).send(to)

#     return Response(status=status.HTTP_204_NO_CONTENT)

# first try

# from rest_framework.views import APIView

# from rest_framework.response import Response

# import requests
# class UserActivationView(APIView):

#     def get (self, request, uid, token):

#         protocol = 'https://' if request.is_secure() else 'http://'

#         web_url = protocol + request.get_host()

#         post_url = web_url + "/auth/users/activate/"

#         post_data = {'uid': uid, 'token': token}

#         result = requests.post(post_url, data = post_data)

#         content = result.text

#         return Response(content)
#mrs
#second try
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
import requests

from account import serializers
class ActivateUser(GenericAPIView):#mrs
    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}
        url = "http://mrsz.pythonanywhere.com/auth/users/activation/"
        response = requests.post(url, data = payload)
        if response.status_code == 204 :

            return Response({"accept":"account activated"}, response.status_code)##*******************************some logic error discription
        elif response.status_code == 403:

            return Response({"Error":"your account already activated"} , status = status.HTTP_403_FORBIDDEN)
        else:
            # return Response(response.json() , status=status.HTTP_202_ACCEPTED)        
            return Response({"Error":"uid or token is invalid"}, status=status.HTTP_400_BAD_REQUEST)


from .serializers import EmailUrlSerializer
from pprint import pprint
class ConfirmPassword(APIView):#mrs

    def post(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token, 'new_password':'mrsmrsmrsmrs' , "re_new_password":'mrsmrsmrsmrs'}

        serializer = EmailUrlSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data)
        payload["new_password"]=serializer.validated_data["password"]
        payload["re_new_password"]=serializer.validated_data["confirm_password"]
        # print(payload)
        url = "http://mrsz.pythonanywhere.com/auth/users/reset_password_confirm/"
        response = requests.post(url, data = payload)
        if response.status_code == 204:
            return Response({"accept":"your password changed"})
        elif response.status_code == 400:
            return Response({"not allow":"bad"})
        else:
            return Response({"exception which not handeled :)"})

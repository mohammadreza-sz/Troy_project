from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from djoser import signals
from djoser.compat import get_user_email
from .serializers import ActivationSerializer

from pprint  import pprint
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
import requests
class ActivateUser(GenericAPIView):#mrs

    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/auth/users/activation/"
        response = requests.post(url, data = payload)

        if response.status_code == 204 :
            return Response({"accept":"account activated"}, response.status_code)##*******************************some logic error discription
        elif response.status_code == 403:
            return Response({"Error":"your account already activated"} , status = status.HTTP_403_FORBIDDEN)
        else:
            # return Response(response.json() , status=status.HTTP_202_ACCEPTED)        
            return Response({"Error":"uid or token is invalid"}, status=status.HTTP_400_BAD_REQUEST)

from urllib.request import Request
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
from rest_framework.decorators import api_view, permission_classes#mrs
from rest_framework.permissions import IsAuthenticated#mrs
# from oauth2_provider.decorators import protected_resource
# @protected_resource()
# @csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])#mrs
def get_role(request):
    role = request.user.role
    return Response({"ROLE":role})
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

from rest_framework.views import APIView
from .models import User as baseuser , UserCode
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMessage, get_connection
from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.hashers import check_password
# from djoser.email
import string    
import random # define the random module  
@api_view(['GET' , 'POST'])#15 by default argument => GET ******** must use permision here
def SendEmailForgotPassword(request):
    if request.method == "POST":
        try:
            user = baseuser.objects.get(email = request.data["email"])
        except :
            return Response("your email does not exist")
        subject = "Troy site"
        S = 6  # number of characters in the string.  
        # call random.choices() string module to find the string in Uppercase + numeric data.  
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
        code  = str(ran)
        # print("The randomly generated string is : " + str(ran)) # print the random data  
        message = ("hello new user , your code is "+code)
        # from_email = request.POST.get("from_email", "")
        # send_mail(subject , message ,"ali", [user.email] , connection=connection).send()
        codeuser = UserCode(user_name = user.username ,code = code)
        codeuser.save()

        send_mail(subject,message, settings.EMAIL_HOST_USER, [user.email,])
        # print("\n \n \n your code is = ",code)
        return Response("email sent")

        # template_name = "email/activation.html"
    else:
        return Response("by")

@api_view(['GET' , 'POST'])#mrs #by default argument => GET      lesson 15
def changepassword(request):
    if request.method == "POST":
        try:
            exist_user_code = UserCode.objects.get(code = request.data["code"])
        except:
            return Response("your code is invalid")
        try:
            user = baseuser.objects.get(username = exist_user_code.user_name)
        except:
            return Response("user doesn't exist")
        password = request.data["password"]
        retype_password = request.data["retype_password"]
        if password != retype_password:
            return Response("password must equall retype_password")
        else:
            old_password = user.password
            if check_password(password , old_password):
                return Response("old password and new password are same! :|")
            else:
                user.set_password(password)
                user.save()
                exist_user_code.delete()
                return Response("your password changed")
    else:
        return Response("nothing")
from django.shortcuts import render
from rest_framework.views import APIView #heln
from rest_framework.generics import GenericAPIView #helen
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

# Create your views here.
# class API(GenericAPIView): #helen
    # serializer_class = UserSerializer
    # def get(self, request):
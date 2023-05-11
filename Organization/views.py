from urllib.request import Request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView #helen
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from djoser import signals
from djoser.compat import get_user_email
from rest_framework.generics import GenericAPIView
import requests
from django.http import HttpResponseBadRequest, HttpResponse
from rest_framework.views import APIView
from Organization import serializers
from .serializers import EmailUrlSerializer

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

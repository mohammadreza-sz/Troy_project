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
from .serializers import *
import base64
from rest_framework.permissions import IsAuthenticated

class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.annotate(avg_rate=Avg('ratesOrg__rate')).all()
    serializer_class = OrganizationSerializer
    ordering_fields = ['-rate']

class OrganizationImageViewSet(ModelViewSet):
    queryset = OrganizationImage.objects.all()
    serializer_class = OrganizationImageSerializer


class RateViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Rate.objects.filter(place = self.kwargs['Organization_pk'])
    def get_serializer_context(self ):
        return {'user_id':self.request.user}
    serializer_class = RateOrgSerializer
    ordering_fields = ['-rate']

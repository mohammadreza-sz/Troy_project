from urllib import request
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
# from account.serializers import UserSerializer
# from .serializers import FavoriteSerializer, PersonSerializer , TripSerializer , CountrySerializer , CitySerializer
from .serializers import *
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
# from .models import Person , Trip , Country , City , Favorite
from .models import *
from datetime import datetime
from .filters import ProductFilter  ,CityFilter#, TripFilter, CountryFilter#mrs
from rest_framework.filters import SearchFilter, OrderingFilter#mrs
from django_filters.rest_framework import DjangoFilterBackend#mrs
class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False , methods=['GET' , 'PUT'])
    def me(self:Person, request):#lesson 60
        (person , created) = Person.objects.get_or_create(id = request.user.id)#********** equal must specify with one '=' not '=='**********
        # person = Person.objects.get(User_id = request.user.id)#********** equal must specify with one '=' not '=='**********
        if request.method == 'GET':
            data = PersonSerializer(person)
            return Response(data.data , status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = PersonSerializer(person , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)
        elif request.method == 'PATCH   ':
            serializer = PersonSerializer(person , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)

class OrganizationViewSet():
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated ]


class ListOrgAPIView(ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CreateOrgAPIView(CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class UpdateOrgAPIView(UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class DeleteOrgAPIView(DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class TourLeaderViewSet():
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer

class ListTourLeaderAPIView(ListAPIView):
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer

class CreateTourLeaderAPIView(CreateAPIView):
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer

class UpdateTourLeaderAPIView(UpdateAPIView):
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer

class DeleteTourLeaderAPIView(DestroyAPIView):
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer


class TripViewSet(CreateModelMixin , RetrieveModelMixin , 
UpdateModelMixin , GenericViewSet ,ListModelMixin , DestroyModelMixin):
    #TODO every one can get but not update
    # queryset = Trip.objects.filter(begin_time__gt =datetime.now() ).all()#mrs change for greater than now
    queryset = Trip.objects.all()#mrs change for greater than now
    # def get_queryset(self):#mrs

    serializer_class = TripSerializer
    # filterset_class = TripFilter  
    # filterset_fields = ['destination_country']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # search_fields = ['destination_country' , 'destination_city']

class CountryViewSet(ModelViewSet):
    # filterset_class = CountryFilter
    filter_backends = [ SearchFilter]
    search_fields = ['country_name']
    queryset = Country.objects.prefetch_related('city_set').all()
    serializer_class = CountrySerializer


class CityViewSet(ModelViewSet):#mrs
    filterset_class = CityFilter#mrs
    filter_backends = [ DjangoFilterBackend]#mrs
    queryset = City.objects.all()
    serializer_class = CitySerializer


# from rest_framework import generics, mixins
class FavoriteView(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    @action(detail=False , methods=['GET' , 'PUT' , 'POST' , 'DELETE'], permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
    def me(self , request):
        favorite = Favorite.objects.filter(common_people_id = request.user.id)
        if request.method == 'GET':
            data = FavoriteSerializer(favorite , many = True )
            return Response(data.data , status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = FavoriteSerializer(favorite , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = FavoriteSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)
        elif request.method == 'DELETE':
            # if product.orderitem_set.count() > 0:
            #     return Response({'error':'foreignkey'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
            favorite.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)

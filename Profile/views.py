from urllib import request
from django.shortcuts import render
#helen{
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
# from account.serializers import UserSerializer
from .serializers import FavoriteSerializer, PersonSerializer , TripSerializer , CountrySerializer , CitySerializer
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
from .models import Person , Trip , Country , City , Favorite

from .filters import ProductFilter  ,CityFilter#, TripFilter, CountryFilter#mrs
from rest_framework.filters import SearchFilter, OrderingFilter#mrs
from django_filters.rest_framework import DjangoFilterBackend#mrs
class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    filterset_class = ProductFilter#mrs
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#mrs

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes=[IsAuthenticated]#helen
    #lookup_field = 'id' #helen
    @action(detail=False , methods=['GET' , 'PUT'])#mrs , permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
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

#}helen

from datetime import datetime#mrs
class TripViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin , DestroyModelMixin):
    #TODO every one can get but not update
    # queryset = Trip.objects.filter(begin_time__gt =datetime.now() ).all()#mrs change for greater than now
    queryset = Trip.objects.all()#mrs change for greater than now
    # def get_queryset(self):#mrs

    serializer_class = TripSerializer

    # filterset_class = TripFilter#mrs
    
    # filterset_fields = ['destination_country']
    filter_backends = [DjangoFilterBackend, OrderingFilter]#mrs
    # search_fields = ['destination_country' , 'destination_city']#mrs


class CountryViewSet(ModelViewSet):#mrs
    # filterset_class = CountryFilter#mrs
    filter_backends = [ SearchFilter]#mrs
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

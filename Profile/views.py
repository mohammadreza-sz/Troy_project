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

from .filters import ProductFilter , TripFilter ,CityFilter#, CountryFilter#mrs
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

# mrs
# from django.forms.models import model_to_dict
# from rest_framework.views import APIView
# from django.db import connection
# from rest_framework.decorators import api_view
# @api_view(['GET'])#mrs     #by default argument => GET  15
# def s_trip(request):
# class s_trip(APIView):
#     def get(self, request):

#         trip = Trip.objects.raw("SELECT * FROM profile_trip pt inner join profile_trip_place_ids ptp where pt.id = ptp.trip_id ")
#         serializer = TripSerializer(trip , many = True)
    # trip = Trip.objects.all().values("id","capacity","capacity","return_transport","departure_date",
    # "departure_date","Description","begin_time","end_time","Price","place_ids","TourLeader_ids").prefetch_related('place_ids' , 'tourleader_ids')


        # query = "SELECT id FROM profile_trip"

        # with connection.cursor() as cursor:
        #     cursor.execute(query)
        #     rows = cursor.fetchall()

        # serializer = TripSerializer(data=rows, many=True)
        # serialized_data = serializer.is_valid(raise_exception=True)

        # return Response(serialized_data)


        # trip = TripSerializer(trip , many = True)
        # trip = model_to_dict(trip ,fields=[field.name for field in trip._meta.fields])
        # return Response(serializer.data)


from datetime import datetime#mrs
class TripViewSet(ModelViewSet):
    #TODO every one can get but not update
    # queryset = Trip.objects.filter(begin_time__gt =datetime.now() ).all()#mrs change for greater than now
    # queryset = Trip.objects.all()#mrs change for greater than now
    def get_queryset(self):#mrs
        # queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids").all()
        queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids" , "TourLeader_ids" , 'destination_city' , 'destination_country' , "TourLeader_ids__orga_id").all()
        return queryset

    # @action(detail=False , methods=['GET' , 'PATCH'])
    # def me(self , request):
    #     trip = Trip.objects.all()#.prefetch_related('place_ids')
    #     return Response(trip)

    serializer_class = TripSerializer

    # filterset_class = TripFilter#mrs
    # filterset_fields = ['destination_country']
    filter_backends = [DjangoFilterBackend, OrderingFilter]#mrs
    # search_fields = ['destination_country' , 'destination_city']#mrs
    ordering_fields = ['Price']



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

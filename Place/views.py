from asyncio.windows_events import NULL
from django.shortcuts import render
from .models import Place , PlaceImage
from .serializer import PlaceImageSerializer, PlaceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from Place import serializer #mrs

class PlaceViewSet(ModelViewSet):#mrs
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceImageViewSet(ModelViewSet):#mrs
    queryset = PlaceImage.objects.all()
    serializer_class = PlaceImageSerializer

@api_view(['GET' , 'POST'])#mrs     #by default argument => GET  15
def get_front_info(request ,place_id = NULL, country_name = NULL , city_name = NULL):
    if place_id == NULL:
        if country_name == NULL :
            data = Place.objects.select_related('city_id' , 'country_id').values("id" ,"name","city_id__country_id__country_name", "city_id__city_name","address" , "description","lan", "lon")#.select_related('country_id').get(id = 1)
        else:
            data = Place.objects.select_related('city_id' , 'country_id').values("id" ,"name","city_id__country_id__country_name", "city_id__city_name","address" , "description","lan", "lon").filter(city_id__city_name=country_name)
            if city_name == NULL:
                data = Place.objects.select_related('city_id' , 'country_id').values("id" ,"name","city_id__country_id__country_name", "city_id__city_name","address" , "description","lan", "lon").filter(city_id__country_id__country_name = country_name )
            else :
                data = Place.objects.select_related('city_id' , 'country_id').values("id" ,"name","city_id__country_id__country_name", "city_id__city_name","address" , "description","lan", "lon").filter(city_id__country_id__country_name = country_name , city_id__city_name=city_name )
    else:
        data = Place.objects.select_related('city_id' , 'country_id').values("id" ,"name","city_id__country_id__country_name", "city_id__city_name","address" , "description","lan", "lon").get(id = place_id)
        


    return Response(data)

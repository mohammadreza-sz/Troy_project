from django.shortcuts import render
from .models import Place , PlaceImage, Rate
from .serializer import PlaceImageSerializer, PlaceSerializer, RateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ModelViewSet #mrs
from rest_framework.permissions import IsAuthenticated#mrs  #61

from django.db.models import Avg

class PlaceViewSet(ModelViewSet):#mrs 
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()   *********************

    # queryset = Place.objects.all()

    queryset = Place.objects.annotate(avg_rate=Avg('rates__rate')).all()
    serializer_class = PlaceSerializer

    ordering_fields = ['-rate']

from Place import serializer #mrs






class PlaceImageViewSet(ModelViewSet):#mrs

    queryset = PlaceImage.objects.all()

    serializer_class = PlaceImageSerializer



class RateViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]#mrs

    # queryset = Rate.objects.all()
    def get_queryset(self):
        return Rate.objects.filter(place = self.kwargs['Place_pk'])

    def get_serializer_context(self ):
        return {'user_id':self.request.user}
    serializer_class = RateSerializer

    ordering_fields = ['-rate']

    





@api_view(['GET'])#mrs     #by default argument => GET  15

def get_specific_placeimage(request , place_idd):

    place_image = PlaceImage.objects.filter(place_id = place_idd).values("place_id" , "image")

    print(place_image)

    return Response(place_image)





from django.db.models import F

@api_view(['GET'])#mrs     #by default argument => GET  15

def get_specific_place(request ,place_id = None, country_name = None , city_name = None):

    place = Place.objects.select_related('city_id' , 'country_id' ).annotate(

        country =F('city_id__country_id__country_name') ,

        city = F('city_id__city_name') ,

        # image = F('placeimage__image')

    ).values("id" ,"name","country", "city","address" , "description","lan", "lon")



    if place_id == None:

        if country_name != None :        

            place =place.filter(city_id__country_id__country_name=country_name)

            if city_name == None:

                place =place.filter(city_id__country_id__country_name = country_name )

            else :

                place =place.filter(city_id__country_id__country_name = country_name , city_id__city_name=city_name )

    else:

        place=place.filter(id = place_id )

    # serializers = PlaceFrontSerializer(place , many = True)

    # return Response(serializers.data)

    return Response(place)

    # place = Place.objects.select_related('city_id' , 'country_id' ).prefetch_related('placeimage_set').annotate(

    #     country =F('city_id__country_id__country_name') ,

    #     city = F('city_id__city_name') ,

    #     image = F('placeimage__image')

    # ).values("id" ,"name","country", "city","address" , "description","lan", "lon" , "image")


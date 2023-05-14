from http import HTTPStatus
from http.client import ResponseNotReady
from pickle import NONE
from django.shortcuts import render

from .models import Place , PlaceImage, Rate

from .serializer import PlaceImageSerializer, PlaceSerializer, RateSerializer

from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from rest_framework.viewsets import ModelViewSet #mrs

from rest_framework import permissions #mrs  #61

from rest_framework import status

from django.db.models import Avg



class PlaceViewSet(ModelViewSet):#mrs 

    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()   *********************



    # queryset = Place.objects.all()



    queryset = Place.objects.annotate(avg_rate=Avg('rates__rate')).all()

    serializer_class = PlaceSerializer



    ordering_fields = ['-rate']



from Place import serializer #mrs

import base64

from django.core.files.base import ContentFile



class PlaceImageViewSet(ModelViewSet):#mrs



    queryset = PlaceImage.objects.all()



    serializer_class = PlaceImageSerializer

    # def post(self, request , *args , **kwargs):

    #     img_b64 = request.post.get('image')

    #     img_data = base64.b64decode(img_b64)

    #     file_name = "my_image.png"

    #     pl_id = request.post.get('place_id')

    #     placeimage = PlaceImage.objects.create(place_id=pl_id)

    #     placeimage.image.save(filename , ContentFile(img_data))

    #     placeimage.save()



    # def get





class RateViewSet(ModelViewSet):

    # permission_classes=[IsAuthenticated]#mrs
    def get_permissions(self):#mrs #61
        if self.request.method in ['POST','PUT','DELETE' , 'PATCH']:
            return [permissions.IsAuthenticated()]
        else:
            return[permissions.AllowAny()]


    # queryset = Rate.objects.all()

    def get_queryset(self):#mrs
        rate = Rate.objects.select_related('place').filter(place = self.kwargs['Place_pk'])
        return rate
    def create(self, request, *args, **kwargs):        

        user = self.request.user
        user_object = Rate.objects.filter(user = user , place = self.kwargs['Place_pk'])
        if user_object.count() >= 1:
            return Response("you can't have duplicate rate" , status=status.HTTP_403_FORBIDDEN)
        else :
            return super().create(request, *args, **kwargs)
        


    def get_serializer_context(self ):

        return {'user_id':self.request.user}

    serializer_class = RateSerializer



    ordering_fields = ['-rate']



    











@api_view(['GET'])#mrs     #by default argument => GET  15



def get_specific_placeimage(request , place_idd):


# def retrieve(self, request, *args, **kwargs):
    # instance = self.get_object()
    # place_image = PlaceImage.objects.filter(place_id = place_idd).values("place_id" , "image")
    # serializer = PlaceImageSerializer(place_image)
    # return Response(serializer.data)
    place_image = PlaceImage.objects.filter(place_id = place_idd).values("place_id" , "image")

    # print(place_image)
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




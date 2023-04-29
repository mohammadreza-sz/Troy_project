from django.shortcuts import render
from .models import Place , PlaceImage
from .serializer import PlaceImageSerializer, PlaceSerializer

from rest_framework.viewsets import ModelViewSet #mrs

class PlaceViewSet(ModelViewSet):#mrs
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceImageViewSet(ModelViewSet):#mrs
    queryset = PlaceImage.objects.all()
    serializer_class = PlaceImageSerializer
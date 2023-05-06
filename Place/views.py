from django.shortcuts import render
from .models import Place , PlaceImage, Rate
from .serializer import PlaceImageSerializer, PlaceSerializer, RateSerializer

from rest_framework.viewsets import ModelViewSet #mrs
from django.db.models import Avg
class PlaceViewSet(ModelViewSet):#mrs
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()   *********************
    # queryset = Place.objects.all()
    queryset = Place.objects.annotate(avg_rate=Avg('rates__rate')).all()

    serializer_class = PlaceSerializer
    ordering_fields = ['-rate']

class PlaceImageViewSet(ModelViewSet):#mrs
    queryset = PlaceImage.objects.all()
    serializer_class = PlaceImageSerializer

class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    ordering_fields = ['-rate']

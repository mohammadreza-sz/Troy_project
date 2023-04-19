from dataclasses import fields
from django_filters.rest_framework import FilterSet
from .models import Person , Trip

class ProductFilter(FilterSet):#mrs
  class Meta:
    model = Person
    fields = {
      'city': ['exact'],
      # 'Id_id': ['gt', 'lt']
    }


class TripFilter(FilterSet):
  class Meta:
    model = Trip
    fields = {
      'Tour_leader_id':['exact'],
      'capacity':['gt' , 'lt'],
      
    }
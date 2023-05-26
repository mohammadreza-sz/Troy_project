from dataclasses import fields

from django_filters.rest_framework import FilterSet

from .models import City, Country, Person , Trip

# from .views import TripViewSet



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

      'origin_city_id':['exact'],
      'TourLeader_ids':['exact'],
      'organization_id':['exact'],
      'destination_city':['exact'],
      'destination_country':['exact'],
      'departure_transport':['iexact'],
      'return_transport':['iexact'],
      'departure_date':['gt' , 'lt' , 'exact'],
      'return_date':['gt' , 'lt' , 'exact'],
      'Price':['gt' , 'lt'],
      'capacity':['gt' , 'lt'],
      'hotel_name':['icontains'],



      # 'destination_city':['contain'],

      


    }


  # def get_search_fields(self, view ,request):

  #   # search_fields = ['destination_country']

  #   if request.query_params.get('destination_city_only'):

  #     return ['destination_city']

  #   if request.query_params.get('destination_country_only'):

  #     return ['destination_country']

  #   return super().get_search_fields(view, request)

  




class CityFilter(FilterSet):

  class Meta:

    model = City

    fields = {

      'city_name':['exact']

    }
from django_filters.rest_framework import FilterSet
from .models import Person

class ProductFilter(FilterSet):#mrs
  class Meta:
    model = Person
    fields = {
      'city': ['exact'],
      # 'Id_id': ['gt', 'lt']
    }

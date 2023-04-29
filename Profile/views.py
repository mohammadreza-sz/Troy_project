from django.shortcuts import render
#helen{
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
# from account.serializers import UserSerializer
from .serializers import PersonSerializer
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter


from rest_framework import viewsets

from .serializers import TripSerializer
from .models import Trip


from django_filters.rest_framework import DjangoFilterBackend
class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes=[IsAuthenticated]#helen
    lookup_field = 'id' #helen
    @action(detail=False , methods=['GET' , 'PUT'])# , permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
    def me(self:Person, request):#lesson 60
        (person , created) = Person.objects.get_or_create(User_id = request.user.id)#********** equal must specify with one '=' not '=='**********
        # person = Person.objects.get(User_id = request.user.id)#********** equal must specify with one '=' not '=='**********
        if request.method == 'GET':
            data = PersonSerializer(person)
            return Response(data.data , status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = PersonSerializer(person , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)


# rate newww

  # Get all trips in random order
class TripViewSet(viewsets.ModelViewSet):
      queryset = Trip.objects.all().order_by('?')
      serializer_class = TripSerializer

#}helen
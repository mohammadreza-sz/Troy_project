from django.shortcuts import render
#helen{
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
# from account.serializers import UserSerializer
from .serializers import PersonSerializer , TripSerializer
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
from .models import Person , Trip

#from .filters import ProductFilter#mrs
#from rest_framework.filters import SearchFilter, OrderingFilter#mrs
#from django_filters.rest_framework import DjangoFilterBackend$mrs
class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
 #   filterset_class = ProductFilter#mrs
  #  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#mrs
    
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes=[IsAuthenticated]#helen
    #lookup_field = 'id' #helen
    @action(detail=False , methods=['GET' , 'PUT'])# , permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
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

#}helen


class TripViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin , DestroyModelMixin):
    #TODO every one can get but not update
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    

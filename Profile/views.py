from urllib import request
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from account.models import User
# from account.serializers import UserSerializer
# from .serializers import FavoriteSerializer, PersonSerializer , TripSerializer , CountrySerializer , CitySerializer
from .serializers import *
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
# from .models import Person , Trip , Country , City , Favorite
from .models import *
from datetime import datetime
from .filters import ProductFilter  ,CityFilter#, TripFilter, CountryFilter#mrs
from rest_framework.filters import SearchFilter, OrderingFilter#mrs
from django_filters.rest_framework import DjangoFilterBackend#mrs
class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False , methods=['GET' , 'PUT'])
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
        elif request.method == 'PATCH   ':
            serializer = PersonSerializer(person , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)

# class OrganizationViewSet():
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     permission_classes = [IsAuthenticated ]


# class ListOrgAPIView(ListAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     # def get_tourl():
#     #     retrun 

# class CreateOrgAPIView(CreateAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer

# class UpdateOrgAPIView(UpdateAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer

# class DeleteOrgAPIView(DestroyAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer


# class TourLeaderViewSet():
#     queryset = TourLeader.objects.all()
#     serializer_class = TourLeaderSerializer




# class ListTourLeaderAPIView(ListAPIView):
#     queryset = TourLeader.objects.all()
#     serializer_class = TourLeaderSerializer
    

# class CreateTourLeaderAPIView(CreateAPIView):
#     queryset = TourLeader.objects.all()
#     serializer_class = TourLeaderSerializer

# class UpdateTourLeaderAPIView(UpdateAPIView):
#     queryset = TourLeader.objects.all()
#     serializer_class = TourLeaderSerializer

# class DeleteTourLeaderAPIView(DestroyAPIView):
#     queryset = TourLeader.objects.all()
#     serializer_class = TourLeaderSerializer


@api_view(['POST'])
def get_tourleaders(request):
    org = Organization.objects.get(name_org = request.data["name_org"])
    if org is not None:
        tl = TourLeader.objects.filter(orga_id= org)
        tl_list = list(tl)
        # print(tl)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if tl is not None:
            serializers = TourLeaderSerializer(tl_list, many = True)
            return Response(serializers.data, status = 200)
    return Response(status = 400)

@api_view(['GET'])
def get_alltourleaders(request):
    tl = TourLeader.objects.all()
    if tl is not None:
        serializers = TourLeaderSerializer(tl, many = True)
        return Response(serializers.data, status = 200)
    return Response(status = 400)


@api_view(['POST'])
def get_toursfromOrg(request):
    org = Organization.objects.get(name_org = request.data["name_org"])
    if org is not None:
        tl = TourLeader.objects.filter(orga_id= org)
        tl_list = list(tl)
        tours = []
        if tl_list is not None:
            for i in tl_list:
                tour = Trip.objects.filter(TourLeader_ids = i) #queryset
                tour_list = list(tour)
                if tour_list is not None:
                    tours.append(tour_list)
        # print(tl)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if tours is not None:
            serializers = TripSerializer(tours, many = True)
            return Response(serializers.data, status = 200)
    return Response(status = 400)


@api_view(['POST'])
def rate_TOURL(request):
    # try:
    #     exist_user_code = UserCode.objects.get(code = request.data["code"])
    # except:
    #     return Response("your code is invalid")
    # try:
    #     user = baseuser.objects.get(username = exist_user_code.user_name)
    # except:
    #     return Response("user doesn't exist")
    user = User.objects.get( username = request.data["username"])
    auth = User.objects.get( username = request.data["TourLeader_username"])

    if request.data["rate"] is not None:
        rateee = request.data["rate"]
    if auth is not None:
        person = Person.objects.get(user_id= auth)
        if person is not None:
            tourl = TourLeader.objects.get(person_id = person)
            if tourl is not None:
                dictt = {}
                dictt["tour_leader"] = tourl.id
                dictt["user"] = user.id
                dictt["rate"] = rateee

                serializers = Rate_TourLSerializer(data = dictt)
                if serializers.is_valid():
                    serializers.save()
                    return Response(200)
    return Response(401)

class TripViewSet(CreateModelMixin , RetrieveModelMixin , 
UpdateModelMixin , GenericViewSet ,ListModelMixin , DestroyModelMixin):
    #TODO every one can get but not update
    # queryset = Trip.objects.filter(begin_time__gt =datetime.now() ).all()#mrs change for greater than now
    queryset = Trip.objects.all()#mrs change for greater than now
    # def get_queryset(self):#mrs

    serializer_class = TripSerializer
    # filterset_class = TripFilter  
    # filterset_fields = ['destination_country']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # search_fields = ['destination_country' , 'destination_city']

class CountryViewSet(ModelViewSet):
    # filterset_class = CountryFilter
    filter_backends = [ SearchFilter]
    search_fields = ['country_name']
    queryset = Country.objects.prefetch_related('city_set').all()
    serializer_class = CountrySerializer


class CityViewSet(ModelViewSet):#mrs
    filterset_class = CityFilter#mrs
    filter_backends = [ DjangoFilterBackend]#mrs
    queryset = City.objects.all()
    serializer_class = CitySerializer


# from rest_framework import generics, mixins
class FavoriteView(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    @action(detail=False , methods=['GET' , 'PUT' , 'POST' , 'DELETE'], permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
    def me(self , request):
        favorite = Favorite.objects.filter(common_people_id = request.user.id)
        if request.method == 'GET':
            data = FavoriteSerializer(favorite , many = True )
            return Response(data.data , status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = FavoriteSerializer(favorite , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = FavoriteSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)
        elif request.method == 'DELETE':
            # if product.orderitem_set.count() > 0:
            #     return Response({'error':'foreignkey'},status= status.HTTP_405_METHOD_NOT_ALLOWED)
            favorite.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)

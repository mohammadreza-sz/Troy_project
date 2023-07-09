
from dataclasses import replace
from email import message
from http.client import ResponseNotReady
from mimetypes import common_types
from unicodedata import decimal
from urllib.request import Request
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
# from account.serializers import UserSerializer
from .serializers import *
from rest_framework.mixins import CreateModelMixin , ListModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.decorators import action #lesson 60
from rest_framework.permissions import IsAuthenticated#61
from rest_framework.response import Response
from rest_framework import status
# from .models import Person , Trip , Country , City , Favorite
from .models import *
from rest_framework.generics import ListAPIView	
from rest_framework.generics import CreateAPIView	
from rest_framework.generics import DestroyAPIView	
from rest_framework.generics import UpdateAPIView	
from rest_framework.decorators import api_view	
from account.models import User
from .filters import *#, CountryFilter#mrs
from rest_framework.filters import SearchFilter, OrderingFilter#mrs
from django_filters.rest_framework import DjangoFilterBackend#mrs
from . import permissions as permi#mrs
from rest_framework.pagination import PageNumberPagination
from .pagination import DefaultPagination
from Profile import pagination
from rest_framework import generics
from account.serializers import UserSerializer

class PersonViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    filterset_class = ProductFilter#mrs
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#mrs
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes=[IsAuthenticated]#helen
    #lookup_field = 'id' #helen
    @action(detail=False , methods=['GET' , 'PUT'])#mrs , permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61

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

    # @api_view(['GET'])#mrs     #by default argument => GET  15

    # def s_trip(request):

    # class s_trip(APIView):

    #     def get(self, request):
    #         trip = Trip.objects.raw("SELECT * FROM profile_trip pt inner join profile_trip_place_ids ptp where pt.id = ptp.trip_id ")

    #         serializer = TripSerializer(trip , many = True)

    # trip = Trip.objects.all().values("id","capacity","capacity","return_transport","departure_date",

    # "departure_date","Description","begin_time","end_time","Price","place_ids","TourLeader_ids").prefetch_related('place_ids' , 'tourleader_ids')
        # query = "SELECT id FROM profile_trip"
        # with connection.cursor() as cursor:
        #     cursor.execute(query)

        #     rows = cursor.fetchall()
        # serializer = TripSerializer(data=rows, many=True)

        # serialized_data = serializer.is_valid(raise_exception=True)
        # return Response(serialized_data)
        # trip = TripSerializer(trip , many = True)

        # trip = model_to_dict(trip ,fields=[field.name for field in trip._meta.fields])

        # return Response(serializer.data)

from rest_framework.views import APIView
from django.utils import timezone

class MyCustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
class user(ListAPIView):
    pagination_class = MyCustomPagination
    serializer_class = CityTripSerializer
    queryset = City.objects.all()
    page_size =3  # Number of items per page

    # def get(self, request):
    #     city = City.objects.all()
    #     serializer = CityTripSerializer(city , many = True )
    #     return Response(serializer.data)
class history_org(APIView):#mrs income of organization for specific range
    permission_classes =[permi.IsOrganization]

    # filterset_class = history_org_Filter#mrs
    # # filterset_fields = ['destination_country']
    # filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]#mrs
    # search_fields = ['hotel_name' , 'Description']#mrs
    # ordering_fields = ['Price' , 'capacity']
    # git commit -m "add history for organization and add filter for it which return total income "
    def get(self , request , begindate = None , enddate=None):
        organization = Organization.objects.get(person_id = request.user)
        if begindate ==None:
            # today = datetime.date.today()
            today = datetime.now().date()#timezone.now().date()
            first_of_this_month = today.replace(day=1)#.replace(hour=0 , minute=0, second=0)
            # if first_of_this_month.month != 1:
            last_of_last_month = first_of_this_month - datetime.now().replace(day =1 ).date()#timezone.timedelta(days=1).date()
            last_of_last_month = last_of_last_month#.replace(hour = 23 , minute=59 , second = 59)
            first_of_last_month = last_of_last_month.replace(day=1)#.replace(hour=0 , minute=0, second=0)
            # else:
            #     last_month = 

            # start_date = timezone.now().replace(day=1) #- timezone.timedelta(days=30)
            # if start_date.month != 1:
            #     start_date = start_date.replace(month = start_date.month - 1)
            #     middle_date = timezone.now()
            # else:
            #     start_date = start_date.replace(year= start_date.year - 1)
            #     start_date.month = 12
            # trip = Trip.objects.filter(organization_id =organization,departure_date__range = (start_date ,timezone.now()))
            trip = Trip.objects.filter(organization_id =organization,departure_date__range = (first_of_last_month,last_of_last_month))
            last_res = 0
            for t in trip:
                if t.Price != None:
                    last_res += t.Price

            trip = Trip.objects.filter(organization_id =organization,departure_date__range = (first_of_this_month,today))
            now_res = 0
            for t in trip:
                if t.Price != None:
                    now_res += t.Price            

            trip = Trip.objects.filter(organization_id = organization)
            total = 0
            for t in trip:
                if t.Price != None:
                    total += t.Price
            return Response({"this month":now_res , "last month":last_res , "total":total})

        else:
            trip = Trip.objects.filter(organization_id =organization,departure_date__range = (begindate , enddate))            
            res =0
            for t in trip:
                if t.Price != None:
                    res += t.Price
            return Response({"res":res})

class history_user(APIView):#mrs
    # permission_classes = [IsAuthenticated]#must add login user must be common people
    permission_classes = [permi.IsPeople]
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             name='user_id',
    #             in_=openapi.IN_QUERY,
    #             type=Type.INTEGER,
    #             description='ID of the user whose history to retrieve',
    #             required=True,
    #         ),
    #     ],
    # )
    def get(self , request):

        c_p_id = CommenPeople.objects.select_related("Id" , "Id__user_id").filter(Id__user_id__id = request.user.id).values('Id').first()["Id"]#what is difference between this  line and next line?

        # c_p_id = CommenPeople.objects.filter(Id__user_id__id = request.user.id).values('Id').first()["Id"]



        queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids" , "TourLeader_ids" , 'destination_city' , 'destination_country' , "TourLeader_ids__orga_id" , "common_people_id").filter(common_people_id__in = [c_p_id]).all()        

        serializer = TripSerializer(queryset , many = True)

        return Response(serializer.data)
    
    # def get(self, request): GPT recommende

    #     c_p_id = CommenPeople.objects.filter(Id__user_id=request.user).values_list('Id', flat=True).first()

    #     queryset = Trip.objects.select_related('origin_city_id__country_id', 'destination_city__country_id', 'TourLeader_ids__orga_id', 'common_people_id__Id__user_id').prefetch_related('place_ids').filter(common_people_id__Id__user_id=request.user)

    #     serializer = TripSerializer(queryset, many=True)

    #     return Response(serializer.data)
from django.shortcuts import get_object_or_404#mrs
from django.db.models import F
class Purchase(APIView):#mrs
    permission_classes = [permi.IsPeople]
    def post(self , request):
        try:
            trip_id = request.data['trip_id']
        except:
            return Response("i want trip id" , status=status.HTTP_400_BAD_REQUEST)
            
        try:
            trip : Trip = Trip.objects.get(id = trip_id)
        except:
            return Response("this trip id is not exist" ,status = status.HTTP_404_NOT_FOUND)
            
        people : CommenPeople = CommenPeople.objects.get(Id__user_id__id =self.request.user.id )#perhaps wnat to optimize
        trip_price = trip.Price
        if people.Id.wallet < trip_price :
            return Response("you don't have enough money!" , status = status.HTTP_403_FORBIDDEN)

        passenger_count = trip.common_people_id.count()
        if passenger_count == trip.capacity :
            return Response("capacity is full!!" , status = status.HTTP_403_FORBIDDEN)
        else:
            # try:
            # people = CommenPeople.objects.get(Id__user_id__id =self.request.user.id )#perhaps wnat to optimize
            # except:

            if people in trip.common_people_id.all():
                return Response("how many time you want register??!!" , status = status.HTTP_403_FORBIDDEN)
            else:
                #must decrease money from wallet*************************************
                person = Person.objects.get(commenpeople = people)
                person.wallet -= trip_price 
                person.save()

                tourleaders = trip.TourLeader_ids.all()
                # tourleaders_object = TourLeader.objects.filter(pk__in =  tourleaders).update(person_id__wallet=F('person_id__wallet') + trip_price)#Note that the __in filter works with any iterable, not just a list. 
                Person.objects.filter(tourleader__in = tourleaders).update(wallet = F('wallet') + Decimal(trip_price * 0.2))

                # for tourleader in tourleaders:
                #     t = TourLeader.objects.get(pk = tourleader)
                #     t.wallet += trip_price * (0.2)
                #     t.save()
                # org = Organization.objects.get(organization = trip.organization_id)
                org = trip.organization_id
                org.wallet += Decimal( trip_price * (0.8))
                # trip.common_people_id.add(people)
                obj:trip_common_people = trip_common_people.objects.create(trip = trip , common_people = people , count = 1)
                obj.save()
                # person.save()
                org.save()

                # serializer = TripSerializer(trep)            
                return Response("add to trip" , status = status.HTTP_200_OK)

class reserve(CreateAPIView):#mrs
    queryset=Passenger.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [permi.IsPeople]
    # def get_serializer_context(self ,trip_id):
    #     return {'trip_id':trip_id}
    def perform_create(self, serializer):
        return serializer.save()
    def create(self , request, trip_id, *args, **kwargs ):
        # try:
        #     trip_id = request.data['trip_id']
        #     count = request.data['count']
        # except:
        #     return Response("give me both trip_id and count!" , status=status.HTTP_400_BAD_REQUEST)
        count =len(request.data)
        try:
            trip : Trip = Trip.objects.get(id = trip_id)
        except:
            return Response("trip id:"+str(trip_id)+" is not exist" ,status = status.HTTP_404_NOT_FOUND)
            
        people : CommenPeople = CommenPeople.objects.get(Id__user_id__id =self.request.user.id )#perhaps wnat to optimize
        trip_price = trip.Price * count
        if people.Id.wallet < trip_price:
            return Response("you must have"+str(trip_price)+" money" , status = status.HTTP_403_FORBIDDEN)

        passenger_count = trip.passenger.count() + count
        if passenger_count > trip.capacity :
            return Response("capacity is"+str(trip.capacity)+"and you can't register!!" , status = status.HTTP_403_FORBIDDEN)
        else:
            # try:
            # people = CommenPeople.objects.get(Id__user_id__id =self.request.user.id )#perhaps wnat to optimize
            # except:

            if people in trip.common_people_id.all():
                return Response("how many time you want register??!!" , status = status.HTTP_403_FORBIDDEN)
            else:
                serializer = ReserveSerializer(data=request.data , many = True)
                serializer.is_valid(raise_exception=True)
                passengers = self.perform_create(serializer)
                trip.passenger.add(*passengers)

                #must decrease money from wallet*************************************
                person = Person.objects.get(commenpeople = people)
                person.wallet -= trip_price
                person.save()

                tourleaders = trip.TourLeader_ids.all()
                # tourleaders_object = TourLeader.objects.filter(pk__in =  tourleaders).update(person_id__wallet=F('person_id__wallet') + trip_price)#Note that the __in filter works with any iterable, not just a list. 
                Person.objects.filter(tourleader__in = tourleaders).update(wallet = F('wallet') + Decimal(trip_price * 0.2))


                org = trip.organization_id
                org.wallet += Decimal( trip_price * (0.8))
                # trip.common_people_id.add(people)
                obj:trip_common_people = trip_common_people.objects.create(trip = trip , common_people = people , count = count)
                obj.save()

                org.save()
                return Response(serializer.data , status = status.HTTP_200_OK)

                # serializer = TripSerializer(trep)            
                # return Response("add to trip" , status = status.HTTP_200_OK)
        
class Increase_people_wallet(APIView):#mrs
    permission_classes = [permi.IsPeople]
    def post(self , request):
        # people_id = request.user.id
        # people_id = CommenPeople.objects.get()
        try:
            # people_id = request.data['people_id']
            money = request.data['money']
        except:
            return Response("i want both people id and money " , status=status.HTTP_400_BAD_REQUEST)

        try:
            person:Person = Person.objects.get(commenpeople__Id__user_id = request.user.id)
        except:
            return Response("i can't find people with this token" , status=status.HTTP_404_NOT_FOUND)
        
        person.wallet += Decimal(money)
        person.save()
        # return Response("his/her wallet is:"+str(person.wallet) , status = status.HTTP_200_OK)
        return Response({"wallet":person.wallet} , status = status.HTTP_200_OK)
        

from django.db import IntegrityError

class RequestToOrg(APIView):#mrs
    permission_classes = [permi.IsPeople]
    def get(self , request , id):#or get
        org = Organization.objects.get(id  =id)
        people = CommenPeople.objects.get(Id__user_id =self.request.user )#perhaps wnat to optimize
        pr = PremiumRequest(common_people = people , organization = org)#organization = org
        try:
            pr.save()
        except IntegrityError:
            return Response("common people id and organization id must be unique!!" ,status=status.HTTP_409_CONFLICT )#409 Conflict:Indicates that the request could not be processed because of conflict in the current state of the resource, such as an edit conflict between multiple simultaneous updates.


        return Response("your request sent")

from django.shortcuts import get_object_or_404

class ShowRequest(APIView):#mrs
    permission_classes = [permi.IsOrganization]
    def get(self , request):
        queryset = PremiumRequest.objects.filter(organization__person_id = request.user).all()
        serializer = PremiumRequestSerializer(queryset , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self , request):
        try:
            obj =PremiumRequest.objects.get(pk = request.data['request_id'] )
        except:
            return Response("can't find request!!" , status=status.HTTP_404_NOT_FOUND)

        if request.data['status'] == 'accept':

            obj.status_choice = 'A'
            obj.save()            
        else:                
            obj.status_choice = 'R'
            obj.save()

        return Response("your change is save!" , status=status.HTTP_200_OK)
            
from datetime import datetime#mrs


class histroy_org2(ListAPIView):#mrs
    permission_classes = [permi.IsOrganization]
    pagination_class = DefaultPagination
    # pagination_class = [PageNumberPagination]        
    serializer_class =OrgHistoryserializer 
    def get_queryset(self):  
        org = Organization.objects.get(person_id = self.request.user)
        return  Trip.objects.filter(organization_id = org , departure_date__lt= datetime.now().date() ).order_by('departure_date').select_related(#this queryset need more optimization
            'origin_city_id','origin_city_id__country_id').prefetch_related(
            'common_people_id', 'destination_city','TourLeader_ids',
            'TourLeader_ids__person_id','TourLeader_ids__person_id__user_id', )#,departure_date__gt = '2000-01-01') #******* it want more optimize for trip_common_people
        # serializer =OrgHistoryserializer(queryset , many =True)
        # return Response(serializer.data)
        
class passenger_list(APIView):#mrs
    permission_classes = [permi.IsOrganization]
    def get(self , request , trip_id:int):
        # tourleaders = Trip.objects.get(pk = trip_id).TourLeader_ids.select_related('person_id' , 'person_id__user_id').all()
        # serializer = Custome2TourLeaderSerializer(tourleaders, many = True)
        passengers = Passenger.objects.filter(trip__pk = trip_id)
        serializer = PassengerListSerializer(passengers, many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)

class TripViewSet(ModelViewSet):

    # permission_classes=[permi.CrudOrganizationReadOther]



    #TODO every one can get but not update

    # queryset = Trip.objects.filter(begin_time__gt =datetime.now() ).all()#mrs change for greater than now

    # queryset = Trip.objects.all()#mrs change for greater than now

    def get_queryset(self):#mrs

        # queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids").all()

        queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids" , "TourLeader_ids" , 'destination_city' , 'destination_country' , "TourLeader_ids__orga_id" , "common_people_id" ).all()

        #queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids" , "TourLeader_ids" , 'destination_city' , 'destination_country' , "TourLeader_ids__orga_id").all()

        return queryset

    def retrieve(self, request, *args, **kwargs):#mrs
        qs = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id').prefetch_related("place_ids" , "TourLeader_ids" , 'destination_city' , 'destination_country' , "TourLeader_ids__orga_id" , "common_people_id").get(id = self.kwargs["pk"])
        serializer = TripSerializer(qs )
        return Response(serializer.data)

    # @action(detail=False , methods=['GET' , 'PATCH'])

    # def me(self , request):

    #     trip = Trip.objects.all()#.prefetch_related('place_ids')

    #     return Response(trip)
    serializer_class = TripSerializer
    filterset_class = TripFilter#mrs
    # filterset_fields = ['destination_country']
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]#mrs
    
    search_fields = ['hotel_name' , 'Description']#mrs
    ordering_fields = ['Price' , 'capacity']

class CustomTrip(ListAPIView):
    serializer_class = CustomeTripSerializer
    filterset_class = CustomeTripFilter
    filter_backends=[DjangoFilterBackend]
    queryset = Trip.objects.select_related('origin_city_id' , 'origin_city_id__country_id' , 'organization_id').prefetch_related("place_ids", 'destination_city' , 'destination_country' ,'passenger').all()
    # def list(self , request):


from rest_framework import permissions
class CountryViewSet(ModelViewSet):#mrs

    # permission_classes = [permi.CrudAdminReadOther]

    # filterset_class = CountryFilter#mrs

    filter_backends = [ SearchFilter]#mrs

    search_fields = ['country_name']

    queryset = Country.objects.prefetch_related('city_set').all()

    serializer_class = CountrySerializer    
    #region
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data, many=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data)
    #endregion
class CityViewSet(ModelViewSet):#mrs
    # permission_classes = [permi.CrudAdminReadOther]
    filterset_class = CityFilter#mrs
    filter_backends = [ DjangoFilterBackend]#mrs
    queryset = City.objects.select_related('country_id').all()
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

@api_view(['GET'])	

def get_orgs(request):	

    orgs = Organization.objects.all()	

    if orgs is not None:	

        serializers = OrganizationSerializer(orgs, many = True)	

        return Response(serializers.data, status = 200)	

    return Response(status = 400)	

@api_view(['POST'])	

def get_tourleaders(request):	

    org = Organization.objects.get(name_org = request.data["name_org"])	

    if org is not None:	

        tl = TourLeader.objects.filter(orga_id= org)	

        tl_list = list(tl)	

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

        if tours is not None:	
            serializers = TripSerializer(tours, many = True)	
            return Response(serializers.data, status = 200)	
    return Response(status = 400)	


class Rate_orgViewSet(ModelViewSet):
    def get_permissions(self):#mrs #61
        if self.request.method in ['POST','PUT','DELETE' ,'PATCH']:
            return [permissions.IsAuthenticated()]
        else:
            return[permissions.AllowAny()]
    def get_queryset(self):
        rate = Rate_Org.objects.select_related('orgg').filter(orgg = self.kwargs.get('Organization_pk'))
        return rate
    def create(self, request, *args, **kwargs):        
        user = self.request.user
        user_object = Rate_Org.objects.filter(user = user , orgg = self.kwargs.get('Organization_pk'))
        if user_object.count() >= 1:
            return Response("you can't have duplicate rate" , status=status.HTTP_403_FORBIDDEN)
        else :
            return super().create(request, *args, **kwargs)
    def get_serializer_context(self ):
        return {'user_username':self.request.user}
    serializer_class = Rate_OrgSerializer
    ordering_fields = ['-rate']

class Rate_TourLViewSet(ModelViewSet):
    def get_permissions(self):#mrs #61
        if self.request.method in ['POST','PUT','DELETE' ,'PATCH']:
  
            return [permissions.IsAuthenticated()]
        else:
            return[permissions.AllowAny()]
    def get_queryset(self):
        rate = Rate_Tour.objects.select_related('tour_leader').filter(tour_leader = self.kwargs.get('TourLeader_pk'))
        return rate
    def create(self, request, *args, **kwargs):        
        user = self.request.user
        user_object = Rate_Tour.objects.filter(user = user , tour_leader = self.kwargs.get('TourLeader_pk'))
        if user_object.count() >= 1:
            return Response("you can't have duplicate rate" , status=status.HTTP_403_FORBIDDEN)
        else :
            return super().create(request, *args, **kwargs)
    def get_serializer_context(self ):
        return {'user_username':self.request.user}
    serializer_class = Rate_TourLSerializer
    ordering_fields = ['-rate']

#helen
class TourLeaderListNotInOrganization(generics.ListAPIView):
    queryset = TourLeader.objects.all()
    def get(self, request):
        # orga_id = self.kwargs.get('orga_id')
        # organization = Organization.objects.filter(id=orga_id).first()
        # if organization:
            # queryset = TourLeader.objects.exclude(orga_id=organization)
        # else:
            # queryset = TourLeader.objects.none()

        q = TourLeader.objects.get(orga_id = None).all()
        return Response(q, status = status.HTTP_200_OK)

class TourLeaderListInOrganization(generics.ListAPIView):
    queryset = TourLeader.objects.all()
    def get(self, request):
        print("1234")
        organization = Organization.objects.filter(person_id = request.user.id).first()
        print("balaye in")
        if organization:
            queryset = TourLeader.objects.filter(orga_id=organization.id).all()
            print("56789")
        else:
            queryset = TourLeader.objects.none()
            print("121231212")
        return Response(queryset, status= status.HTTP_200_OK)



# to send requests for tourleaders that are not in the list..
class RequestCreate(generics.CreateAPIView):
    serializer_class = RequestSerializer

    def create(self, request, *args, **kwargs):
        # Get the organization and tour leader ids from the request data
        orga_id = request.data.get('orga_id')
        tl_id = request.data.get('tl_id')
        # Check if the tour leader exists and is not already part of the organization
        tourleader = TourLeader.objects.filter(id=tl_id).exclude(orga_id=orga_id).first()
        if not tourleader:
            return Response({'error': 'Tour leader does not exist or is already part of the organization.'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the organization exists
        organization = Organization.objects.filter(id=orga_id).first()
        if not organization:
            return Response({'error': 'Organization does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a new Request object
        request_obj = Request.objects.create(orga_id=organization, tl_id=tourleader)
        # Serialize and return the new Request object
        serializer = RequestSerializer(request_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# delete a tourleader
class TourLeaderDeleteFromOrganization(generics.DestroyAPIView):

    def delete(self, request, orga_id, tl_id):
        # Get the organization instance
        organization = Organization.objects.filter(id=orga_id).first()
        if not organization:
            return Response({'error': 'Organization does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the tour leader is part of the organization
        tourleader = TourLeader.objects.filter(id=tl_id, orga_id=organization).first()
        if not tourleader:
            return Response({'error': 'Tour leader is not part of the organization.'}, status=status.HTTP_400_BAD_REQUEST)
        # Remove the tour leader from the organization
        organization.tourleader.remove(tourleader)
        # Serialize and return the updated organization
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

#helen

class OrganizationViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    # filterset_class = ProductFilter#mrs
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#mrs
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=False , methods=['GET' , 'PUT'])
    def me(self:Organization, request):
        print(request.user.id)
        org  = Organization.objects.filter(person_id = request.user.id).first()
        if request.method == 'GET':
            data = OrganizationSerializer(org)
            return Response(data.data , status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            serializer = OrganizationSerializer(org , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)

        elif request.method == 'PATCH   ':
            serializer = OrganizationSerializer(org , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)



class TourLeaderViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet ,ListModelMixin):
    # filterset_class = ProductFilter#mrs
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#mrs
    queryset = TourLeader.objects.all()
    serializer_class = TourLeaderSerializer
    @action(detail=False , methods=['GET' , 'PUT'])
    def me(self:TourLeader, request):
        (tl , created) = TourLeader.objects.get_or_create(id = request.user.id)
        
        if request.method == 'GET':
            data = TourLeaderSerializer(tl)
            return Response(data.data , status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            serializer = TourLeaderSerializer(tl , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)

        elif request.method == 'PATCH   ':
            serializer = TourLeaderSerializer(tl , data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'opreation':'succesfully update'} | serializer.data ,status =status.HTTP_200_OK)


class CustomCountryCity(ListAPIView):
    filterset_class = CustomCountryCityFilter#mrs
    filter_backends = [DjangoFilterBackend]#mrs
    serializer_class =CustomCountryCitySerializer 
    queryset = Country.objects.all()
    # def list(self , request):
        # country = Country.objects.all()
        # serializer = CustomCountryCitySerializer(country , many = True)
        # return Response(serializer.data , status=status.HTTP_200_OK)
        

class CustomPouria(ListAPIView):
    filterset_class = CustomCountryCityFilter#mrs
    filter_backends = [DjangoFilterBackend]#mrs
    serializer_class =CustomPouriaSerializer 
    queryset = Country.objects.all()
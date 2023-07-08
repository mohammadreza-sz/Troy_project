from ast import expr_context
from dataclasses import fields
from email.policy import default
from itertools import count
from re import search
from unittest.util import _MAX_LENGTH
from wsgiref import validate
from rest_framework import serializers
from Place.models import Place
# from .models import Organization, Person, TourLeader , Trip , Country , City , Favorite
from .models import *
from django.conf import settings
from django.db.models import Avg

class PersonSerializer(serializers.ModelSerializer):#lesson 59
    # gender = serializers.BooleanField(initial=True)
    #profile_image = Base64ImageField(required=False) #helen
    class Meta:
        model = Person
        fields =['birth_date' , 'country' , 'city' , 'gender',
         'bio' , 'registration_date', 'profile_image' ]

class CityTripSerializer(serializers.ModelSerializer):

    # country_name = serializers.SerializerMethodField()
    country_name = serializers.StringRelatedField(source = 'country_id')
    class Meta:
        model = City

        fields =( 'country_name','city_name')

    # def get_country_name(self, obj):

    #     return obj.country_id.country_name

class PlaceTripSerializer(serializers.ModelSerializer):

    country = serializers.SerializerMethodField()

    city =  serializers.SerializerMethodField()

    class Meta:

        model = Place

        fields = ['name', 'city' , 'country']

    # city_id = CityTripSerializer()

    def get_city(self , obj):

        return obj.city_id.city_name

    def get_country(self , obj):

        return obj.city_id.country_id.country_name

class TransportSerializer(serializers.Serializer):#mrs

    TRANSPORT_CHOICES = [

        ('A' , 'airplane'),

        ('S' , 'ship'),

        ('B' , 'bus'),

        ('T' , 'train')
    ]

    departure_transport = serializers.ChoiceField(choices=TRANSPORT_CHOICES)

    return_transport = serializers.ChoiceField(choices=TRANSPORT_CHOICES)

class DestinationSerializer(serializers.Serializer):

    country_name = serializers.CharField(max_length = 30)

    city_name = serializers.CharField(max_length = 30)

# def to_internal_value(self, data):
#     trans_dict = data.pop('transport')
#     departure_transport = trans_dict.pop('departure_transport')
#     return_transport_display = trans_dict.pop('return_transport')
#     return_transport = dict(MyModel.TRANSPORT_CHOICES).get(return_transport_display)
#     data['departure_transport'] = departure_transport
#     data['return_transport'] = return_transport

#     return data
from rest_framework.response import Response
class TripSerializer(serializers.ModelSerializer):#mrs
    destination= CityTripSerializer(many = True , source  = 'destination_city')#mrs if want to obtain destination from place_ids ************ this approach can't handle city name which exist in multiple country
    # transport = TransportSerializer(source = '' )#return (departure_transport , return_transport)within object
    # transport = serializers.CharField(default = "C") #we can use this instead use nested serializer
    

    premium = serializers.SerializerMethodField()
    def get_premium(self , obj:Trip):#mrs
        result = []
        
        for people in obj.common_people_id.all():
            # count :int = 1
            try:
                count = trip_common_people.objects.get(trip = obj ,common_people = people).count
            except:
                return Response({"what the hell?!?!@#*&"})
                # count =1
                
            
            try:
                p = PremiumRequest.objects.get(common_people = people , organization = obj.organization_id)
                
                res = p.status_choice
                if res =='A' :
                    result.append({'is_premium':True, 'name': people.Id.user_id.username , 'count':count})
                else:
                    result.append({'is_premium':False, 'name': people.Id.user_id.username , 'count':count})
            except:
                result.append({'is_premium':False, 'name': people.Id.user_id.username , 'count':count})

            

        # return [{'is_premium': people.premium, 'name': people.Id.user_id.username} for people in obj.common_people_id.all()]
        return result

    class Meta:
        model = Trip
        # fields = ['id'  , 'origin_city_id' ,'destination_city','destination_country','departure_transport','return_transport','departure_date','return_date' ,'Description', 'capacity' , 'Price', 'place_ids','organization_id','TourLeader_ids']
        # fields = ['id'  , 'origin' ,'destination','departure_date','transport','return_date' ,'Description', 'capacity' , 'Price', 'place_ids','organization_id','TourLeader_ids' , 'image' , 'hotel_name']
        fields = ['id' ,'origin','destination','departure_transport','return_transport','departure_date','return_date','Description','capacity', 'Price' ,'place_ids','organization_id','TourLeader_ids' ,'image' , 'hotel_name' , 'premium']

    origin = CityTripSerializer(source = 'origin_city_id')
    # origin = serializers.SerializerMethodField(source = 'origin_city_id')
    # def get_origin(self , obj):
    #     if obj.origin_city_id != None:
    #         return obj.origin_city_id.city_name
    #     else :
    #         return None
    def to_representation(self, instance):#return (departure_transport , return_transport)within object
        data = super().to_representation(instance)
        departure_transport = data.pop('departure_transport')
        return_transport = data.pop('return_transport')
        data['transport'] = {
            # 'departure_transport':instance.get_departure_transport_display(),#get_departure_transport_display for return human readable of choice field
            # 'return_transport': instance.get_return_transport_display()
            'departure_transport':departure_transport,
            'return_transport': return_transport

        }
        return data
    def to_internal_value(self, data):
        if 'transport' in data:#when use patch method , maybe transport doesn't exist in data
            trans_dict = data.pop('transport')
            if("departure_transport" in trans_dict):#maybe just want update departure_transport
                departure_transport = trans_dict.pop('departure_transport')
                data['departure_transport']=departure_transport

            if("return_transport" in trans_dict):#maybe just want update departure_transport
                return_transport = trans_dict.pop('return_transport')
                data['return_transport']=return_transport        
        
        # departure_transport =self.convert_choice_field(departure_transport)
        # return_transport = self.convert_choice_field(return_transport)
        # print("departure",departure_transport)
        
        # print("data:",data)

        # data['departure_transport']=value.get_foo
        # data['return_transport']=return_transport
        return super().to_internal_value(data )
        # return data
    def convert_choice_field(self , str:str):
        if str == "bus":
            return 'B'
        if str == "airplane":
            return 'A'
        if str == "ship":
            return 'S'
        if str == "train":
            return 'T'

    def create(self , validated_data):
        origin_data = validated_data.pop('origin_city_id')
        city_name = origin_data.pop('city_name')
        try:
            city = City.objects.get(city_name = city_name)
        except:
            raise ValidationError({"error": "this city name for origin doesn't exist"})
        destination_data = validated_data.pop('destination_city' , [])
        places_data = validated_data.pop('place_ids', [])
        tourleader_data = validated_data.pop('TourLeader_ids', [])
        # destiantion_id = (for dest in destination_data)
        # validated_data['origin_city_id'] = city
        trip = Trip.objects.create( origin_city_id = city,**validated_data)
        try:
            trip.destination_city.set([City.objects.get(city_name = dest['city_name']).id for dest in destination_data])
        except:
            raise ValidationError({"error":"this city name doesn't exist for destination field"})
        trip.place_ids.set([place.id for place in places_data])
        # trip.place_ids.set(places for place in places_data)
        trip.TourLeader_ids.set([str(tourl.person_id_id) for tourl in tourleader_data])

        return trip
    def update(self, instance, validated_data):
        if 'origin_city_id' in validated_data:
            try:
                origin = validated_data.pop('origin_city_id')
                city_name = origin.pop('city_name')
                city = City.objects.get(city_name = city_name)
            except:
                raise ValidationError({"error": "this city name for origin doesn't exist"})

            instance.origin_city_id =city
            # instance.save()
        if 'destination_city' in validated_data:
            try:
                destination_data = validated_data.pop('destination_city' , [])
                instance.destination_city.set([City.objects.get(city_name = dest['city_name']).id for dest in destination_data])
            except:
                raise ValidationError({"error":"this city name doesn't exist for destination field"})

            instance.save()
            
        # instance.content = validated_data.get('content', instance.content)
        # instance.created = validated_data.get('created', instance.created)
        instance = super().update(instance, validated_data)
        # instance.save()
        return instance
        # transport_data = validated_data.pop('transport')
        # validated_data.push(transport_data['departure_transport'])
        # validated_data.push(transport_data['return_transport'])

        # trip =Trip.objects.create(**validated_data)
        # return trip

        # user = User.objects.create(**validated_data)
        # Profile.objects.create(user=user, **profile_data)
        # return user
    # def save(self):

    ##############################

    # def get_transport(self , obj):

    #     return f"{obj.departure_transport},{obj.return_transport}"



    # organization_id = serializers.SerializerMethodField()#mrs for get organization from tourleader_ids but has logic error

    # def get_organization_id(self , obj:Trip):

    #     tour_leader = obj.TourLeader_ids.first()

    #     if tour_leader:

    #         return tour_leader.orga_id.id

    #     return None

    #     return obj.TourLeader_ids.all().first().orga_id.name_org

    #     return [tour_leader.orga_id.name_org for tour_leader in obj.TourLeader_ids.all()]

class CustomeTourLeaderSerializer(serializers.ModelSerializer):#mrs
    image = serializers.SerializerMethodField()
    tourleader_name = serializers.SerializerMethodField()
    tourleader_id = serializers.PrimaryKeyRelatedField(source = 'person_id' , read_only = True)
    
    class Meta:
        model = TourLeader
        fields = ['image','tourleader_name','tourleader_id' ]

    def get_image(self , obj:TourLeader):
        return obj.person_id.profile_image
    def get_tourleader_name (self , obj:TourLeader):
        return obj.person_id.user_id.first_name
class OrgHistoryserializer(serializers.ModelSerializer):#mrs
    registered = serializers.SerializerMethodField()
    # number_of_page = serializers.SerializerMethodField()
    multiple_dest = serializers.SerializerMethodField()    
    class Meta:
        model = Trip
        fields = ['id','multiple_dest','TourLeader_ids' ,'origin' , 'destination',"Price" ,"capacity","registered" , "departure_date" , "image" ]

    TourLeader_ids = CustomeTourLeaderSerializer(many = True)
    origin = CityTripSerializer(source = 'origin_city_id')
    destination= CityTripSerializer(many = True , source  = 'destination_city')#mrs if want to obtain destination from place_ids ************ this approach can't handle city name which exist in multiple country
    def get_registered(self , obj:Trip):
        count:int = 0        
        passengers = obj.trip_common_people_set.filter(trip = obj).all()
        for j in passengers:
            count+=j.count
        return count

    def get_multiple_dest(self ,obj):
        if obj.destination_city.count()>1:
            return True
        else:
            return False
    # def get_number_of_page(obj):
    #     return 

class tripserializer(serializers.Serializer):

    id = serializers.IntegerField()

class CitySerializer(serializers.ModelSerializer):
    # country_name = serializers.StringRelatedField(source = 'country_id' , read_only = False)
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ['city_name' , 'country_name']
    def get_country_name(self, obj):
        return obj.country_id.country_name
    
    # def to_internal_value(self, data):
    #     return data
    # def create(self , validated_data):
    #     country_name = validated_data.pop('country_name')
    #     country = Country.objects.create(country_name = country_name)
    #     city = City.objects.create(country_id = country , **validated_data)
    #     return city

class OrganizationSerializer(serializers.ModelSerializer):	
    # country_nameOrg = serializers.SerializerMethodField()	
    mean_rate = serializers.SerializerMethodField(default=0)

    class Meta:	

        model = Organization	

        fields = ["person_id",
                    "name_org" ,
                    "description" ,
                    "city_id", 
                    "logo", 
                    "Address", 
                    "Phone", 
                    "rates", 
                    "wallet",
                    "mean_rate"]

        # read_only_fields = ["user_id"]	
    def get_mean_rate(self, obj):
        rates = obj.rate_org.all()
        mean_rate = rates.aggregate(Avg('rate'))['rate__avg']
        return mean_rate or 0
    # def get_country_nameOrg(self, obj):	
    #     pass
    #     return obj.city_id.country_id.country_name	

class  Rate_OrgSerializer(serializers.ModelSerializer):	
    usernm = serializers.CharField(source='user.username', read_only=True)
    # user_name = serializers.SerializerMethodField()
    class Meta:	

        model = Rate_Org	
        # fields = "__all__"	
        fields = [
            'id',
            'orgg',
            'usernm',
            # 'user_name',
            'rate',
        ]

    def get_user_name(self, obj):
        return obj.user.username
    def create(self , validated_data):
        # user_id = self.context['user_id']#mrsz
        usernm = self.context['user_username']
        return Rate.objects.create(user = usernm  ,**validated_data)

class TourLeaderSerializer(serializers.ModelSerializer):	
    mean_rate = serializers.SerializerMethodField(default = 0)
    class Meta:
        model = TourLeader
        fields = ['person_id', 'orga_id', 'rates', 'rate_no', 'joindDate', 'phonetl', 'mean_rate']

    def get_mean_rate(self, obj):
        rates = obj.rate_tour.all()
        mean_rate = rates.aggregate(Avg('rate'))['rate__avg']
        return mean_rate or 0

class  Rate_TourLSerializer(serializers.ModelSerializer):	
    usernm = serializers.CharField(source='user.username', read_only=True)
    # user_name = serializers.SerializerMethodField()
    class Meta:
        model = Rate_Tour #this is for tourleader not for tours..
        fields = [
            'id',
            'tour_leader',
            'usernm',
            # 'user_name',
            'rate',
        ]

    def get_user_name(self, obj):
        return obj.user.username
    def create(self , validated_data):
        # user_id = self.context['user_id']#mrsz
        usernm = self.context['user_username']#mrsz
        return Rate.objects.create(user = usernm  ,**validated_data)

class CountrySerializer(serializers.ModelSerializer):#mrs
    class Meta:
        model = Country
        fields = ['country_name' , 'city_set' ]#] 'city_set__city_name']
    city_set = CitySerializer(read_only = True , many = True)

class FavoriteSerializer(serializers.ModelSerializer):
    # common_people_id = serializers.CharField()
    class Meta:
        model = Favorite
        fields = ['favorite' , 'common_people_id']

class PremiumRequestSerializer(serializers.ModelSerializer):#mrs
    class Meta:
        model = PremiumRequest
        fields = ['organization' , 'common_people' , 'status_choice']
        
            
# class Custome2TourLeaderSerializer(serializers.ModelSerializer):
class PassengerListSerializer(serializers.ModelSerializer):#mrs
    # firstname = serializers.SerializerMethodField()
    # lastname = serializers.SerializerMethodField()
    # phone = serializers.SerializerMethodField()
    # national_code = serializers.SerializerMethodField()

    class Meta:
        # model = TourLeader
        model = Passenger
        fields = ['firstname' , 'lastname' , 'phone' , 'national_code']
    # def get_firstname(self ,obj):
    #     return obj.person_id.user_id.first_name
    # def get_lastname(self ,obj):
    #     return obj.person_id.user_id.last_name
    # def get_phone(self , obj):
    #     return obj.person_id.user_id.phone
    # def get_national_code(self , obj):
    #     return obj.person_id.user_id.national_code

    
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        # fields = ('id', 'orga_id', 'tl_id', 'status', 'created_at', 'updated_at')
        
class ReserveSerializer(serializers.ModelSerializer):#mrs
    class Meta:
        model = Passenger
        fields = ['firstname' , 'lastname' , 'national_code' , 'phone']
    # def create(self , validated_data):
    #     trip_id = self.kwargs.pop('trip_id', None)

    # def __init__(self, *args, **kwargs):
    #     # trip_id = kwargs.pop('trip_id', None)
    #     trip_id =self.context['view'].kwargs.get('trip_id')
    #     super().__init__(*args, **kwargs)
    #     if trip_id is not None:
    #         self.fields['trip'] = serializers.IntegerField(initial=trip_id, write_only=True)

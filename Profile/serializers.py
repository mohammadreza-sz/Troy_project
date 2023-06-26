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
# from base64.fields import Base64ImageField #helen
#helen{
#class Base64ImageField(serializers.ImageField):
#    def to_internal_value(self, data):
#        if isinstance(data, six.string_types):
#            if 'data:' in data and ';base64,' in data:
#               header, data = data.split(';base64,')
#            try:
#                decoded_file = base64.b64decode(data)
#            except TypeError:
#                self.fail('invalid_image')
#            file_name = str(uuid.uuid4())[:16]
#            file_extension = self.get_file_extension(file_name, decoded_file)
#           complete_file_name = "%s.%s" % (file_name, file_extension, )
 #           data = ContentFile(decoded_file, name=complete_file_name)
#            return super(Base64ImageField, self).to_internal_value(data)
#    def get_file_extension(self, file_name, decoded_file):
 #       import imghdr
#        extension = imghdr.what(file_name, decoded_file)
#        extension = "jpg" if extension == "jpeg" else extension
#
#        return extension
#    def to_representation(self, instance):
#        if instance.name:
#            return(settings.BASE_URL+reverse('download', args=[instance.name]))
#        else:
#            return None
#}helen
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



# class TripTourLeaderSerializer(serializers.ModelSerializer):#mrs

#     name = serializers.SerializerMethodField()

#     class Meta:

#         model = TourLeader

#         fields = 'Id' , 'name'

#     def get_name(self,obj):

#         return obj.Id.user_id.id



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
class TripSerializer(serializers.ModelSerializer):#mrs
    destination= CityTripSerializer(many = True , source  = 'destination_city')#mrs if want to obtain destination from place_ids ************ this approach can't handle city name which exist in multiple country
    # transport = TransportSerializer(source = '' )#return (departure_transport , return_transport)within object
    # transport = serializers.CharField(default = "C") #we can use this instead use nested serializer
    

    premium = serializers.SerializerMethodField()
    def get_premium(self , obj):
        result = []
        for people in obj.common_people_id.all():
            try:
                p = PremiumRequest.objects.get(common_people = people , organization = obj.organization_id)
                res = p.status_choice
                if res =='A' :
                    result.append({'is_premium':True, 'name': people.Id.user_id.username})
                else:
                    result.append({'is_premium':False, 'name': people.Id.user_id.username})
            except:
                result.append({'is_premium':False, 'name': people.Id.user_id.username})

            

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
    country_nameOrg = serializers.SerializerMethodField()	

    user_id = PersonSerializer()	

    class Meta:	

        model = Organization	

        fields = "__all__"	

        read_only_fields = ["user_id"]	

    def get_country_nameOrg(self, obj):	

        return obj.city_id.country_id.country_name	

    # def get_tours(self, obj):	

        # objj = obj.tourleader.set_tour.all()

# class  Rate_OrgSerializer(serializers.ModelSerializer):	
#     class Meta:	
#         model = Rate_Org	
#         fields = "__all__"	


class  Rate_OrgSerializer(serializers.ModelSerializer):	
    usernm = serializers.CharField(source='user.username', read_only=True)
    user_name = serializers.SerializerMethodField()
    class Meta:	

        model = Rate_Org	
        # fields = "__all__"	
        fields = [
            'id',
            'orgg',
            'usernm',
            'user_name',
            'rate',
        ]

    def get_user_name(self, obj):
        return obj.user.username
    def create(self , validated_data):
        # user_id = self.context['user_id']#mrsz
        user_name = self.context['user_username']
        return Rate.objects.create(user = user_name  ,**validated_data)

class TourLeaderSerializer(serializers.ModelSerializer):	

    # organ_name = serializers.SerializerMethodField()	

    # rateTL_num = serializers.SerializerMethodField()	

    # trips = serializers.SerializerMethodField()	

    # ratees = serializers.SerializerMethodField()	

    class Meta:	

        model = TourLeader	

        fields = "__all__"	

        read_only_fields = ["rates", "rate_no"]	

    # def get_organ_name(self, obj):	

    #     return obj.orga_id.name	

    # def get_rateTL_num(self, obj):	

    #     # self.rate_no = 	

    #     if obj.rates_Tour is not None:	

    #         self.rate_no = len(obj.rate_tour)	

    #     else:	

    #         self.rate_no = 0	

    # def get_ratees(self , obj):	

        # return obj.rates	

    # def get_rate_no(self, obj):	

        # return len()	

    # def get_trips(self , obj):	

        # objj = obj.tourleader.all()	

        # return TripSerializer(objj).data

class  Rate_TourLSerializer(serializers.ModelSerializer):	
    usernm = serializers.CharField(source='user.username', read_only=True)
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Rate_Tour #this is for tourleader not for tours..
        fields = [
            'id',
            'tour_leader',
            'usernm',
            'user_name',
            'rate',
        ]

    def get_user_name(self, obj):
        return obj.user.username
    def create(self , validated_data):
        # user_id = self.context['user_id']#mrsz
        user_name = self.context['user_username']#mrsz
        return Rate.objects.create(user = user_name  ,**validated_data)

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
    # def create(self  ,validated_data):#validated_data ->dictionary #lesson 17
    #     favorite = Favorite(**validated_data)#umpack dictionary
    #     favorite.common_people_id = 1
    #     favorite.save() 
    #     return favorite

class PremiumRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumRequest
        fields = ['organization' , 'common_people' , 'status_choice']
        
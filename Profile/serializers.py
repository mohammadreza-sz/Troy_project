from dataclasses import fields
from itertools import count
from re import search
from rest_framework import serializers
from Place.models import Place

# from .models import Organization, Person, TourLeader , Trip , Country , City , Favorite
from .models import *

from django.conf import settings
# from base64.fields import Base64ImageField 
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

class PersonSerializer(serializers.ModelSerializer):#lesson 59
    class Meta:
        model = Person
        fields =['birth_date' , 'country' , 'city' , 'gender',
         'bio' , 'registration_date', 'profile_image' ]

class OrganizationSerializer(serializers.ModelSerializer):
    country_nameOrg = serializers.SerializerMethodField()
    user_id = PersonSerializer()
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ["user_id"]


# ["name_org","description" ,"logo","Address","Phone","rates"]

    def get_country_nameOrg(self, obj):
        return obj.city_id.country_id.country_name
    # def get_tours(self, obj):
        # objj = obj.tourleader.set_tour.all()

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


#helen

class  Rate_TourLSerializer(serializers.ModelSerializer):
    # rateTL_num = serializers.SerializerMethodField()
    # tour_leader_username = serializers.SerializerMethodField()
    # user_username = serializers.SerializerMethodField()
    class Meta:
        model = Rate_Tour
        # fields = ["rate"]
        fields = "__all__"
    # def get_tour_leader_username(self , obj):
    #     return obj.tour_leader.Id.user_id.username

class CityTripSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = 'country_name','city_name'
    def get_country_name(self, obj):
        return obj.country_id.country_name
class  Rate_OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate_Org
        fields = "__all__"
class CityTripSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = 'country_name','city_name'
    def get_country_name(self, obj):
        return obj.country_id.country_name
class  Rate_TourLSerializer(serializers.ModelSerializer):
    # rateTL_num = serializers.SerializerMethodField()
    # tour_leader_username = serializers.SerializerMethodField()
    # user_username = serializers.SerializerMethodField()
    class Meta:
        model = Rate_Tour
        # fields = ["rate"]
        fields = "__all__"
    # def get_tour_leader_username(self , obj):
    #     return obj.tour_leader.Id.user_id.username

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

class DestinationSerializer(serializers.Serializer):
    country_name = serializers.CharField(max_length = 30)
    city_name = serializers.CharField(max_length = 30)
class TripSerializer(serializers.ModelSerializer):#mrs
    # destination= CityTripSerializer(many = True , source  = 'destination_city')#mrs if want to obtain destination from place_ids

    # transport = TransportSerializer(source = '' , read_only = True)#return (departure_transport , return_transport)within object
    class Meta:
        model = Trip
        # fields = ['id' , 'destination_country' ,'destination_city' , 'origin_country',  'origin_city' , 'begin_time' , 'end_time' , 'capacity']
        fields = "__all__" #['id' , 'destination_country' ,'destination_city' , 'origin_country',  'origin_city' , 'begin_time' , 'end_time' , 'capacity']

       
    # def to_representation(self, instance):#return (departure_transport , return_transport)within object
    #     data = super().to_representation(instance)
    #     data['transport'] = {
    #         'departure_transport':instance.get_departure_transport_display(),
    #         'return_transport': instance.get_return_transport_display()
    #     }
    #     return [data]
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
    class Meta:
        model = City
        fields = ['city_name' , 'country_id']

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

class  Rate_OrgSerializer(serializers.ModelSerializer):	
    class Meta:	
        model = Rate_Org	
        fields = "__all__"	


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
    # rateTL_num = serializers.SerializerMethodField()	
    # tour_leader_username = serializers.SerializerMethodField()	
    # user_username = serializers.SerializerMethodField()	
    class Meta:	
        model = Rate_Tour	
        # fields = ["rate"]	
        fields = "__all__"	
    # def get_tour_leader_username(self , obj):	
    #     return obj.tour_leader.Id.user_id.username	
    # def user_username(self , obj):	
    #     return obj.user.username	
    # def get_rateTL_num(self, obj):	
    #     self.rate_no = len(obj.rates_tour)

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

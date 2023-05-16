from dataclasses import fields
from itertools import count
from re import search
from rest_framework import serializers
# from .models import Person , Trip , Country , City , Favorite, Organization, TourLeader
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
    # tour_leaders = serializers.SerializerMethodField()
    tour_leaders = "TourLeaderSerializer(many = True)"
    # tours = serializers.SerializerMethodField()
    country_nameOrg = serializers.SerializerMethodField()
    user_id = PersonSerializer()
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ["user_id"]

    def get_country_nameOrg(self, obj):
        return self.city_id.country_id.country_name
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


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        # fields = ['id' , 'destination_country' ,'destination_city' , 'origin_country',  'origin_city' , 'begin_time' , 'end_time' , 'capacity']
        fields = "__all__" #['id' , 'destination_country' ,'destination_city' , 'origin_country',  'origin_city' , 'begin_time' , 'end_time' , 'capacity']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name' , 'country_id']

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

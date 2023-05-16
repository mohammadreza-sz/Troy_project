from dataclasses import fields

from itertools import count

from re import search

from rest_framework import serializers

from Place.models import Place

from .models import Organization, Person, TourLeader , Trip , Country , City , Favorite

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

    # user =



#helen
class CityTripSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = 'country_name','city_name'
    def get_country_name(self, obj):
        return obj.country_id.country_name


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

class TripSerializer(serializers.ModelSerializer):#mrs
    # destination= CityTripSerializer(many = True , source  = 'destination_city')#mrs if want to obtain destination from place_ids

    # transport = TransportSerializer(source = '' , read_only = True)#return (departure_transport , return_transport)within object
    class Meta:
        model = Trip
        fields = ['id'  , 'origin_city_id' ,'destination_city','destination_country','departure_transport','return_transport','departure_date','return_date' ,'Description', 'capacity' , 'Price', 'place_ids','organization_id','TourLeader_ids']
    #     fields = ['id'  , 'origin' ,'destination','departure_date','transport','return_date' ,'Description', 'capacity' , 'Price', 'place_ids','organization_id','TourLeader_ids']
    # origin = CityTripSerializer(source = 'origin_city_id')

       
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

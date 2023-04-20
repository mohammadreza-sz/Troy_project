from dataclasses import fields
from itertools import count
from re import search
from rest_framework import serializers
from .models import Person , Trip , Country , City
from django.conf import settings
# from base64.fields import Base64ImageField #helen
#helen{
class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:16] 
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

            return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    def to_representation(self, instance):
        if instance.name:
            return(settings.BASE_URL+reverse('download', args=[instance.name]))
        else:
            return None

#}helen
class PersonSerializer(serializers.ModelSerializer):#lesson 59
    # gender = serializers.BooleanField(initial=True)

    profile_image = Base64ImageField(required=False) #helen
    class Meta:
        model = Person
        fields =['birth_date' , 'country' , 'city' , 'gender',
         'bio' , 'registration_date', 'profile_image' ]
    # user = 
#helen

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['destination_country' ,'destination_city' , 'origin_country',  'origin_city' , 'begin_time' , 'end_time' , 'capacity']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name' , 'country_id']


class CountrySerializer(serializers.ModelSerializer):#mrs
    class Meta:
        model = Country
        fields = ['country_name' , 'city_set' ]#] 'city_set__city_name']
    city_set = CitySerializer(read_only = True , many = True)

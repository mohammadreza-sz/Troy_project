
# from ..Profile.serializers import CitySerializer
from .models import Place , PlaceImage
from rest_framework import serializers
class PlaceImageSerializer(serializers.ModelSerializer):#mrs
    class Meta:
        model = PlaceImage
        fields =['id' , 'image' , 'place_id']


class PlaceSerializer(serializers.ModelSerializer):#mrs 59
    # placeimage_set = PlaceImageSerializer(many = True , read_only = True)
    placeimage_set = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='image'
    )
    # city = CitySerializer()
    # city_id = serializers.CharField(max_length = 50)
    # country_id= serializers.CharField(max_length = 50)
    class Meta:
        model = Place
        fields = [
                # 'country_name',
                # 'city_id__city_name',
                'city_id',           
                'name',
                'address',
                'description',
                'lan',
                'lon',
                'placeimage_set',
                'rate',
                'rate_no',
            ]
        # read_only_fields = ['rate', 'rate_no']
        


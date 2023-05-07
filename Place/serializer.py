

# from ..Profile.serializers import CitySerializer

from dataclasses import fields

from .models import Place , PlaceImage, Rate

from rest_framework import serializers

class PlaceImageSerializer(serializers.ModelSerializer):#mrs

    class Meta:

        model = PlaceImage

        fields =['id' , 'image' , 'place_id']





class PlaceSerializer(serializers.ModelSerializer):#mrs 59

    # placeimage_set = PlaceImageSerializer(many = True , read_only = True)

    # placeimage_set = serializers.SlugRelatedField(

    #     many=True,

    #     read_only=True,

    #     slug_field='image'

    # )

    # city = CitySerializer()

    # city_id = serializers.CharField(max_length = 50)

    # country_id= serializers.CharField(max_length = 50)

    avg_rate = serializers.ReadOnlyField()
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    class Meta:

        model = Place

        fields = [

                'country_name',

                'city_name',

                # 'city_id',           

                'id',

                'name',

                'address',

                'description',

                'lan',

                'lon',

                # 'placeimage',
                'rate_no',

                'avg_rate',



            ]

    def get_city_name(self, obj):
        return obj.city_id.city_name
    def get_country_name(self, obj):
        return obj.city_id.country_id.country_name
    



class RateSerializer(serializers.ModelSerializer):#mrs 59

    class Meta:

        model = Rate

        fields = [

            'place',

            'user',

            'rate'

        ]
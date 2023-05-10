

# from ..Profile.serializers import CitySerializer

from dataclasses import fields

from .models import Place , PlaceImage, Rate

from rest_framework import serializers
# import base64
class PlaceImageSerializer(serializers.ModelSerializer):#mrs

    # image = serializers.SerializerMethodField()
    # def create(self, validated_data):
    #     image_string = validated_data.pop('image')
    #     image_bytes = base64.b64decode(image_string)
    #     validated_data['image'] = image_bytes
    #     return super().create(validated_data)

    
    # def get_image_data(self, obj):
    #     return obj.get_image_as_base64()

    # def create(self, validated_data):
    #     image_data = validated_data.pop("image_data", None)
    #     instance = super().create(validated_data)
    #     if image_data:
    #         instance.save_image_to_field(image_data)
    #     return instance

    # def update(self, instance, validated_data):
    #     image_data = validated_data.pop("image_data", None)
    #     instance = super().update(instance, validated_data)
    #     if image_data:
    #         instance.save_image_to_field(image_data)
    #     return instance
            
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

    user = serializers.CharField(read_only = True)

    class Meta:

        model = Rate

        fields = [

            'id',

            'place',

            'user',

            'rate'

        ]

    def create(self , validated_data):

        user_id = self.context['user_id']

        return Rate.objects.create(user = user_id  ,**validated_data)
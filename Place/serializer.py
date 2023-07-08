from dataclasses import fields
# from account.models import User 
from django.db.models import Avg
from .models import *
from rest_framework import serializers
# import base64
class PlaceImageSerializer(serializers.ModelSerializer):#mrs
    #region mrs
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
    #endregion
    class Meta:

        model = PlaceImage

        fields =['id' , 'image' , 'place_id']

class PlaceSerializer(serializers.ModelSerializer):#mrs 59
    #region mrs
    # placeimage_set = PlaceImageSerializer(many = True , read_only = True)

    # placeimage_set = serializers.SlugRelatedField(

    #     many=True,

    #     read_only=True,

    #     slug_field='image'

    # )
    # username = serializers.SerializerMethodField()	
    
    # city = CitySerializer()

    # city_id = serializers.CharField(max_length = 50)

    # country_id= serializers.CharField(max_length = 50)
    #endregion
    mean_rate = serializers.SerializerMethodField(default = 0)
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    # comment_no = serializers.SerializerMethodField()
    # rate_no = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
                'country_name',
                'city_name',
                'city_id',           
                'id',
                'name',
                'address',
                'description',
                'lan',
                'lon',
                # 'placeimage',
                'mean_rate',
            ]
        # fields = "__all__"
    def get_mean_rate(self, obj):
        rates = obj.rates.all()
        mean_rate = rates.aggregate(Avg('rate'))['rate__avg']
        return mean_rate or 0
    # def get_comment_no(self):
    #     self.comment_number = self.comments.count()
    #     self.save()
    # def get_rate_no(self):
    #     # self.rate_no = len(rates)
    #     self.rate_no = self.rate.count()
    def get_city_name(self, obj):

        return obj.city_id.city_name

    def get_country_name(self, obj):

        return obj.city_id.country_id.country_name
    # def get_username(self , obj):	
        # return obj.user.username	

class RateSerializer(serializers.ModelSerializer):#mrs 59

    usernm = serializers.CharField(source='user.username', read_only=True)
    # user_name = serializers.SerializerMethodField()
    # user = serializers.CharField(read_only = True)
    class Meta:
        model = Rate
        fields = [
            'id',
            'place',
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

class UserCommentSerializer(serializers.ModelSerializer):	
    class Meta:	
        model = User	
        fields = ['username']

class ReplySerializer(serializers.ModelSerializer):	
    user = UserCommentSerializer(read_only=True)	
    class Meta:	
        model = Comment	
        fields = ['id', 'created_date', 'text', 'user', 'place']	
        # fields = "__all__"
        read_only_fields = ['id', 'created_date', 'user']	
    def create(self, validated_data):	
        request = self.context.get("request")	
        validated_data['place_id'] = self.context.get("place")	
        validated_data['parent_id'] = self.context.get("parent")	
        validated_data['user'] = request.user	
        return super().create(validated_data)	
    def update(self, instance, validated_data):	
        validated_data['created_date'] = datetime.now()	
        return super().update(instance, validated_data)


# class CommentSerializer(serializers.ModelSerializer):	
#     replies = ReplySerializer(read_only=True, many=True)	
#     user = UserCommentSerializer(read_only=True)	
#     class Meta:	
#         model = Comment	
#         fields = ['id', 'created_date', 'text', 'user', 'replies']	
#         read_only_fields = ['id', 'created_date']	
#     def create(self, validated_data):	
#         request = self.context.get("request")	
#         validated_data['place_id'] = self.context.get("place")	
#         validated_data['user'] = request.user	
#         instance = super().create(validated_data)	
#         instance.place.update_comment_no()	
#         return instance	
#     def update(self, instance, validated_data):	
#         validated_data['created_date'] = datetime.now()	
#         return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user', 'place', 'replies']
        read_only_fields = ['id', 'created_date', 'user', 'place']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['place_id'] = self.context.get("place")
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)
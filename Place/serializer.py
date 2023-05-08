
# from ..Profile.serializers import CitySerializer
from dataclasses import fields
from .models import *
from rest_framework import serializers
from datetime import datetime
from account.models import User
class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields =['id' , 'image' , 'place_id']

class PlaceSerializer(serializers.ModelSerializer):
    placeimage_set = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='image'
    )
    place_name = serializers.SerializerMethodField('get_place_name')
    # is_liked_new = serializers.SerializerMethodField('get_is_liked')

    avg_rate = serializers.ReadOnlyField()
    class Meta:
        model = Place
        fields =  "__all__" 
        read_only_fields = [
            'rate', 
            'rate_no', 
            'comment_number',
            'like_number']
        def get_place_name(self, Place):
            return Place.name

        # def get_is_liked(self, experience):
        #     request = self.context.get("request")
        #     print(request)
        #     if request.user.is_anonymous == False:
        #         user = request.user
        #     else:
        #         return False
        
        #     likes = Like.objects.filter(user=user, experience=experience)
        #     if len(likes) > 0:
        #         return True
        #     else:
        #         return False
    
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = [
            'place',
            'user',
            'rate'
        ]

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user', 'place']
        
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = self.context['user']
        # need to change
        validated_data['place'] = self.context['place']
        return super().create(validated_data)



class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image']


class ReplySerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user']
        read_only_fields = ['id', 'created_date', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['place_id'] = self.context.get("place")
        validated_data['place_id'] = self.context.get("parent")
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(read_only=True, many=True)
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user', 'replies']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['plac_id'] = self.context.get("place")
        validated_data['user'] = request.user
        instance = super().create(validated_data)
        instance.experience.update_comment_no()
        return instance

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)

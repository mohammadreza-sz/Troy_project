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
    rate_no = serializers.ReadOnlyField()
    comment_number = serializers.ReadOnlyField()
    city_name = serializers.SerializerMet
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = "__all__"  
        read_only_fields = ['avg_rate', 'comment_number', 'rate_no','user']

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
                'comment_number',
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
        validated_data['parent_id'] = self.context.get("parent")
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
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['user'] = request.user
        instance = super().create(validated_data)
        instance.place.update_comment_no()
        return instance

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)

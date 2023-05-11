from .models import *
from rest_framework import serializers

class UserSerializer(BaseUserSerializer):#mrs#59
    class Meta(BaseUserSerializer.Meta):
        fields =['id', 'username', 'email']

class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer): 
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'email', 'username', 'password')

class EmailUrlSerializer(serializers.Serializer):#mrs
    password = serializers.CharField(max_length =255 )
    confirm_password = serializers.CharField(max_length =255)
    
    def validate (self, data):
        if data['password'] != data['confirm_password']:
            return serializers.ValidationError('passwords do not match')
        return data #-> dictionary

class Origanization(serializers.ModelsSerializer):
    rate_no = serializers.ReadOnlyField()
    city_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ['avg_rate', 'rate_no','user']

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
        return Rate.objects.create(user = user_id ,**validated_data)

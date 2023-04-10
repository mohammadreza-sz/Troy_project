from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer ,UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer 
from rest_framework import serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()
# from django.conf import settings

# class UserCreateSerializer(BaseUserCreateSerializer):#helen
#     class Meta(BaseUserCreateSerializer.Meta):
#         # model = settings.AUTH_USER_MODEL
#         fields = ('id', 'email', 'username', 'password' , 'first_name' , 'last_name')

class UserSerializer(BaseUserSerializer):#mrs#59
    class Meta(BaseUserSerializer.Meta):
        fields =['id' , 'email' , 'username' , 'first_name' , 'last_name']
    username = serializers.CharField(max_length = 40)

    # email = serializers.EmailField(read_only = True)#if want to avoid to modify its own email

class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):#mrs
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'email', 'username' , 'password')#,'first_name' , 'last_name')
    # email = serializers.EmailField(read_only = True)#if want to avoid to modify its own email
    # password = serializers.CharField(read_only = True)
    # re_new_password = serializers.CharField(read_only = True)

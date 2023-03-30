from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer ,UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer 
# from django.contrib.auth import get_user_model
# User = get_user_model()
# from django.conf import settings

class UserCreateSerializer(BaseUserCreateSerializer):#helen
    class Meta(BaseUserCreateSerializer.Meta):
        # model = settings.AUTH_USER_MODEL
        fields = ('id', 'email', 'username', 'password' , 'first_name' , 'last_name')

class UserSerializer(BaseUserSerializer):#mrs#59
    class Meta(BaseUserSerializer.Meta):
        fields =['id' , 'email' , 'username' , 'first_name' , 'last_name']

class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):#mrs
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'email', 'username','first_name' , 'last_name','password')
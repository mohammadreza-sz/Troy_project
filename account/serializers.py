from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer ,UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer
from djoser.serializers import  PasswordResetConfirmRetypeSerializer as BasePasswordResetConfirmRetypeSerializer
    # 'activation': 'djoser.serializers.ActivationSerializer',

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
    password = serializers.CharField()
    re_new_password = serializers.CharField()


class EmailUrlSerializer(serializers.Serializer):#mrs
    password = serializers.CharField(max_length =255 )
    confirm_password = serializers.CharField(max_length =255)
    
    def validate (self, data):
        if data['password'] != data['confirm_password']:
            return serializers.ValidationError('passwords do not match')
        return data #-> dictionary

        
# class PasswordResetConfirmRetypeSerializer(BasePasswordResetConfirmRetypeSerializer):
#     class Meta(BasePasswordResetConfirmRetypeSerializer.Meta):






#mrs
# from djoser.conf import settings
# from djoser import utils
# from django.contrib.auth import authenticate, get_user_model
# from rest_framework.exceptions import ValidationError
# User = get_user_model()

# class UidAndTokenSerializer(serializers.Serializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.initial_data['uid'] = self.context.get("uid")
#         self.initial_data['token'] = self.context.get("token")

#     uid = serializers.CharField()
#     token = serializers.CharField()

#     default_error_messages = {
#         "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
#         "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
#     }

#     def validate(self, attrs):
#         validated_data = super().validate(attrs)
        
#         # uid validation have to be here, because validate_<field_name>
#         # doesn't work with modelserializer
#         try:
#             uid = utils.decode_uid(self.initial_data.get("uid", ""))
#             self.user = User.objects.get(pk=uid)
#         except (User.DoesNotExist, ValueError, TypeError, OverflowError):
#             key_error = "invalid_uid"
#             raise ValidationError(
#                 {"uid": [self.error_messages[key_error]]}, code=key_error
#             )

#         is_token_valid = self.context["view"].token_generator.check_token(
#             self.user, self.initial_data.get("token", "")
#         )
#         if is_token_valid:
#             return validated_data
#         else:
#             key_error = "invalid_token"
#             raise ValidationError(
#                 {"token": [self.error_messages[key_error]]}, code=key_error
#             )

# from django.core import exceptions
# class ActivationSerializer(UidAndTokenSerializer):
#     default_error_messages = {
#         "stale_token": settings.CONSTANTS.messages.STALE_TOKEN_ERROR
#     }

#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         if not self.user.is_active:
#             return attrs
#         raise exceptions.PermissionDenied(self.error_messages["stale_token"])


# class ActivationSerializer(BaseActivationSerializer):
#     uid = serializers.CharField(intial=context.get("uid"))
#     token = serializers.CharField(intial =context.get("token"))
#     def get_uid(self) -> str : 
#         return self.context.get("uid")
#     def get_token(self) -> str :
#         return self.context.get("token")

#     class Meta(BaseActivationSerializer.Meta):




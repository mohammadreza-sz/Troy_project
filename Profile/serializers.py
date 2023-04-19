from rest_framework import serializers
from .models import Person
class PersonSerializer(serializers.ModelSerializer):#lesson 59
    # gender = serializers.BooleanField(initial=True)
    class Meta:
        model = Person
        fields =['birth_date' , 'country' , 'city' , 'gender',
         'bio' , 'registration_date' , 'image' , 'first_name' , 'last_name']#helen


class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):#mrs

    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'email', 'username'  ,'first_name' , 'last_name', 'password')
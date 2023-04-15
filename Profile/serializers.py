class PersonSerializer(BaseUserSerializer):#lesson 59
    class Meta(BaseUserSerializer.Meta):
        fields =['id' , 'birth_date' , 'country' , 'city' , 'gender',
         'bio' , 'registration_date' , 'profile_image']

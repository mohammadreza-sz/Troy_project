from django.db import models
from django.contrib.auth.models import AbstractUser #lesson 47

    # class UserAccountManager(BaseUserManager):
    #     def create_user(self , email, name, password = None):
    #         if not email:
    #             raise ValueError('Users must have an email address')
    #         email = self.normalize_email(email)
    #         # normalize_email : BRayan@gmail.com --> brayan@gmail.com
    #         user = self.model(email = email, name = name) 

    #         user.set_password(password)
    #         user.save()

    #         return user

class User(AbstractUser):#mrs       #lesson 47 we can use this user model instead of default user which django use
    email = models.EmailField(unique=True)
    

    # email = models.EmailField(max_length = 255, unique = True)

#helen
    # objects = UserAccountManager()

    # USERNAME_FIELD = 'email'
    # REQIERED_FIELDS = ['name']
    
    # def get_full_name(self):
    #     return self.name
    # def get_short_name(self):
    #     return self.name
    # def __str__(self):
    #     return self.email
#helen
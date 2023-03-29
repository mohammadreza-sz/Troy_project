from django.db import models
from django.contrib.auth.models import AbstractUser #lesson 47

class User(AbstractUser):#mrs       #lesson 47 we can use this user model instead of default user which django use
    email = models.EmailField(unique=True)

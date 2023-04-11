from django.db import models
from django .cintrib.auth.models import User

class Person(models.Model):
    birth_date : models.DateField(null = True)
    country : models.CharField(max_length = 255)
    city : models.CharField(max_length = 255)
    gender : models.BooleanField()
    bio : models.TextField()
    registration_date : models.DateField(auth_now = True)
    image : models.ImageField(upload_to = 'pics', default = 'default.svg')
    #phone
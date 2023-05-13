from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.db import models
from Organization.models import Organization
from Place.models import Place

class Person(models.Model):    
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , null = True)
    birth_date = models.DateField(null = True)
    country = models.CharField(max_length = 50 , null=True) 
    city = models.CharField(max_length = 50 ,null=True)   
    gender = models.BooleanField(null=True)
    bio = models.TextField(null=True)
    registration_date = models.DateField(auto_now= True)
    profile_image = models.TextField(blank=True, null=True)#helen
    def __str__(self):
        return str(self.user_id)

class CommenPeople(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)
    friend_id = models.ManyToManyField("CommenPeople")
    def __str__(self) -> str:
        return str(self.Id)
        
class TourLeader(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)
    orga_id = models.ForeignKey(Organization, on_delete = models.SET_NULL, null= True)
    
    # deleted = models.BooleanField(default=False)
    # comment : models.TextField(max_length = 250)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=40)
    # rate = models.IntegerField(default = 0)  # in baraye khode tour leader hast..(faghat afrade sherkat konande)

class Trip(models.Model):
    Trip_ID = models.IntegerField().primary_key
    place_id = models.ForeignKey(Place, on_delete = models.SET_NULL, null= True)
    TourLeader_ids = models.ForeignKey(TourLeader, on_delete = models.CASCADE)
    # destination_country = models.CharField(max_length = 30 , null = True)
    # destination_city = models.CharField(max_length = 30 , null = True)
    # origin_country = models.CharField(max_length = 30 , null = True)
    origin_city = models.CharField(max_length = 30 , null = True)
    # destinations_city
    # Transport = 
    # Departure = 
    # return = --> i dont remember it..
    # Organization_id = --> you must get it from tour leader.. 
    Description = models.TextField(null = True)
    # begin_time = models.DateTimeField(null = True)
    # end_time = models.DateTimeField(null = True)
    capacity = models.IntegerField(null = True)
    # image =
    Price = models.IntegerField()
    # Place_id

# class Transport(models.Model):
#     pass

class Country(models.Model):
    country_name = models.CharField(null = True , max_length=30)
    def __str__(self) -> str:
        return self.country_name

class City(models.Model):
    city_name = models.CharField(null = True, max_length=30)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE , null = True)
    
    tripCity = models.ForeignKey(Trip, on_delete = models.CASCADE, null = True)
    def __str__(self) -> str:
        return self.city_name

class Post(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete = models.CASCADE, null= True)
    caption = models.TextField()

class Post_image(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True)
    post_image = models.TextField(blank=True, null=True)


class Favorite(models.Model):
    favorite = models.TextField(null =True)
    common_people_id = models.ForeignKey(CommenPeople , on_delete=models.CASCADE)
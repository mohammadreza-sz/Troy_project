from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.db import models#mrs

# CRUD baraye safar tavassote organization va assign kardane ye tour leader baraye oon

class Person(models.Model):
    Id = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , default = 0, primary_key= True)
    birth_date = models.DateField(null = True)
    country = models.CharField(max_length = 50 , null=True) 
    city = models.CharField(max_length = 50 ,null=True)   
    gender = models.BooleanField(null=True)
    bio = models.TextField(null=True)
    registration_date = models.DateField(auto_now= True)
    profile_image = models.TextField(blank=True, null=True)#helen
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
#helen {
class CommenPeople(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)
    friend_id = models.ManyToManyField("CommenPeople")

class Organization(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE)
    # (ye ghesmat bayad dashte bashe ke tour leader hash ro neshoon bede...)

class TourLeader(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)
    orga_id = models.ForeignKey(Organization, on_delete = models.SET_NULL, null= True)
    # deleted = models.BooleanField(default=False)
    # comment : models.TextField(max_length = 250)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=40)
    # rate = models.IntegerField(default = 0)  # in baraye khode tour leader hast..(faghat afrade sherkat konande)

class Trip(models.Model):
    # vali dar halate koli dar Trip ha zakhire shode bashand...
    Tour_leader_id = models.ForeignKey(TourLeader, on_delete=models.SET_NULL, null= True)
    destination = models.CharField(max_length = 30)
    origin = models.CharField(max_length = 30)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.IntegerField()
class Post(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete = models.CASCADE, null= True)
    caption = models.TextField()
    
class Post_image(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True)
    post_image = models.TextField(blank=True, null=True)


# deleted ro dobare roosh fekr kon..
# }helen
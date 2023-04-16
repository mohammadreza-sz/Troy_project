from tkinter import CASCADE

from django.db import models

from django.conf import settings

from django.db import models#mrs

from base64.fields import Base64ImageField #helen
### User ### 



# {edit profile}

# CRUD baraye safar tavassote organization va assign kardane ye tour leader baraye oon

class Person(models.Model):

    User = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , null = False)

    birth_date = models.DateField(null = True)

    country = models.CharField(max_length = 255 , null=True) 

    city = models.CharField(max_length = 255 ,null=True)   

    gender = models.BooleanField(null=True)

    bio = models.TextField(null=True)

    registration_date = models.DateField(auto_now= True)

    profile_image = models.TextField(blank=True, null=True)#helen





#helen {

# class CommenPeople(models.Model):

#     Person = models.OneToOneField(Person , on_delete=CASCADE )

#     friend_id : models.IntegerField()

#     foreignkey_to_account : models.IntegerField()



# class TourLeader(models.Model):

#     id : models.IntegerField()

#     orga_id : models.IntegerField()

#     # expired_time : models.DateField.auto_now_add()

#     post : models.ImageField() #helen -- > bayad betoone chand ta bezare..(az safarhaye rafte shode)

#     # galery tor...

#     # add to db{

#     # comment : models.TextField(max_length = 250)

#     # rate : models.IntegerField(default = 0)  # in baraye khode tour leader hast..(faghat afrade sherkat konande)



#     # safarhaye rafte shode ro bayad ba ax o inha neshoon bede

#     # leza bayad ye ghesmate post dashte bashim.

#     # baraye safarhaye rafte shode bayad adam hayee ke toye oon safar boodan betoonan rate bedan..





# class Organization(models.Model):

#     id : models.IntegerField()

#     post : models.ImageField() # helen -- > bayad betoone chand ta bezare..(baraye safarhayee ke gharare bere..)

#     # (ye ghesmat bayad dashte bashe ke tour leader hash ro neshoon bede...)





# class OrgImage(models.Model):

#     id : models.IntegerField()

#     org_id : models.IntegerField()

#     image : models.ImageField()



# class Trip(models.Model):

#     # {safar hayee ke gharare dashete bashim inja gofte mishe(ba tavajoh be time)..}

#     # bayad begim age tarikh nagzashte tooye organization neshoonesh bede..

#     # vali dar halate koli dar Trip ha zakhire shode bashand...

#     id : models.IntegerField()

#     tour_leader_id : models.IntegerField()

#     destination : models.TextField(max_length = 255)

#     origin : models.TextField()

#     duration_time : models.DateField()

#     begin_time : models.DateField()

#     end_time : models.DateField()

#     capacity : models.IntegerField()

# class Untitled(models.Model):

#     trip_id : models.DateField()

#     peaple_id : models.DateField()

# }helen
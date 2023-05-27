from statistics import mode
from tkinter import CASCADE
from account.models import User
from django.db import models
from django.conf import settings
from django.db import models#mrs
from Place import models as place_model
from django.core.validators import MaxValueValidator, MinValueValidator
# CRUD baraye safar tavassote organization va assign kardane ye tour leader baraye oon
class Person(models.Model):    
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , null = True)#mrs 
    birth_date = models.DateField(null = True)
    country = models.CharField(max_length = 50 , null=True) 
    city = models.CharField(max_length = 50 ,null=True)   
    gender = models.BooleanField(null=True)
    bio = models.TextField(null=True)
    registration_date = models.DateField(auto_now= True)
    profile_image = models.TextField(blank=True, null=True)#helen
    # def __str__(self):
    #     return str(self.user_id)
#helen {
class CommenPeople(models.Model):
    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)
    friend_id = models.ManyToManyField("CommenPeople")
    def __str__(self) -> str:
        return str(self.Id)
class Country(models.Model):#mrs
    country_name = models.CharField(null = True , max_length=30)
    def __str__(self) -> str:
        return self.country_name
class City(models.Model):#mrs
    city_name = models.CharField(null = True, max_length=30)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE , null = True)
    def __str__(self) -> str:

        return self.city_name


class Organization(models.Model):	
    # user_id = models.OneToOneField(settings.AUTH_USER_MODEL ,	
            # on_delete=models.CASCADE , null = True, related_name= 'orguser')    	
    person_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,	
        null = True)	
    	
    name_org = models.CharField(max_length=200,unique=True , null = True)	
    description = models.TextField(null = True)	
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)# city, country	
    logo = models.TextField(blank = True, null = True)	
    Address =models.CharField(max_length=255 , null = True)	
    Phone = models.CharField(max_length=20 , null = True)	
    rates = models.IntegerField(default=0, blank=True)	

class Rate_Org(models.Model):	
    orgg = models.ForeignKey(	
        Organization, on_delete=models.CASCADE, related_name='rate_org')	
    user = models.ForeignKey(	
        User, on_delete=models.CASCADE, related_name='rates_org')	
    rate = models.IntegerField(default=0, 	
        validators=[MinValueValidator(0), MaxValueValidator(5)])	

    def __str__(self):
        return f"{self.user.username} rated {self.rate} to {self.orgg.name_org}"
        # return f"rated {self.rate} to {self.place.name}"

class TourLeader(models.Model):	
    person_id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)	
    orga_id = models.ForeignKey(Organization, on_delete = models.CASCADE,	
     null= True, related_name = "tourleader")	
    rates = models.IntegerField(default=0, blank=True)	
    rate_no = models.IntegerField(default=0, blank=True)	
    joindDate = models.DateTimeField(auto_now=True)	
    phonetl = models.CharField(max_length=20 , null = True)	
class Rate_Tour(models.Model):	
    tour_leader = models.ForeignKey(	
        TourLeader, on_delete=models.CASCADE, related_name='rate_tour')	
    user = models.ForeignKey(	
        User, on_delete=models.CASCADE, related_name='rates_tour')	
    rate = models.IntegerField(default=5, 	
        validators=[MinValueValidator(0), MaxValueValidator(5)])	
    def __str__(self):	
        return f"{self.user.email} rated {self.rate} to {self.tour_leader.person_id.city}"	

from django.core.exceptions import ValidationError#mrs
class Trip(models.Model):
    place_ids = models.ManyToManyField(place_model.Place , blank = True)#mrs can't use null here , must use blank
    TourLeader_ids = models.ManyToManyField(TourLeader,   blank = True)#must be in same organization
    organization_id = models.ForeignKey(Organization , on_delete=models.DO_NOTHING,null = True)
    destination_country = models.ManyToManyField(Country , related_name= 'countries')
    destination_city =  models.ManyToManyField(City , related_name='cities')
    # origin_country_id = models.ForeignKey(Country , on_delete=models.PROTECT , null = True)
    origin_city_id =  models.ForeignKey(City , on_delete=models.PROTECT , null = True)
    # image = get from placeimage
    airplane = 'A'
    ship = 'S'
    bus = 'B'
    train = 'T'
    TRANSPORT_CHOICES = [
        (airplane , 'airplane'),
        (ship , 'ship'),
        (bus , 'bus'),
        (train , 'train')

    ]
    departure_transport= models.CharField(max_length=1 , choices=TRANSPORT_CHOICES , null = True )
    return_transport = models.CharField(max_length=1 , choices=TRANSPORT_CHOICES , null = True )
    departure_date = models.DateTimeField(null = True)
    return_date =  models.DateTimeField(null = True)
  # destinations_city
    # Transport = 
    # Departure = 
    # return = --> i dont remember it..
    # Organization_id = --> you must get it from tour leader.. 
    Description = models.TextField(null = True)
    # begin_time = models.DateTimeField(null = True)#must delete it 
    # end_time = models.DateTimeField(null = True)#must delete it 
    capacity = models.IntegerField(null = True , validators=[MinValueValidator(1) , MaxValueValidator(50)])
    

    Price = models.IntegerField(null = True , validators=[MinValueValidator(5) , MaxValueValidator(5000)])
    # Place_id
    def clean(self):#mrs
        if self.return_date and self.departure_date :
            if self.return_date < self.departure_date:
                raise ValidationError('Return date cannot be earlier than departure date.')
        
    # Tour_leader_id = models.ForeignKey(TourLeader, on_delete=models.SET_NULL, null= True)
    # destination_country = models.CharField(max_length=30, null = True)
    # destination_city = models.CharField(max_length=30, null = True)
    # origin_country = models.CharField(max_length=30, null = True)
    # origin_city = models.CharField(max_length=30, null = True)
    # begin_time = models.DateTimeField(null = True)
    # end_time = models.DateTimeField(null = True)
    # capacity = models.IntegerField(null = True)

    # image = models.ImageField(upload_to = "profile/imaged" , null = True)#mrs
class Post(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete = models.CASCADE, null= True)
    caption = models.TextField()

class Post_image(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True)
    post_image = models.TextField(blank=True, null=True)

# deleted ro dobare roosh fekr kon..



# }helen



class Favorite(models.Model):
    favorite = models.TextField(null =True)
    common_people_id = models.ForeignKey(CommenPeople , on_delete=models.CASCADE)
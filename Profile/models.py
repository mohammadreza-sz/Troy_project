from statistics import mode
from tkinter import CASCADE
from account.models import User
from django.db import models
from django.conf import settings
from django.db import models#mrs
from Place import models as place_model
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal#mrs
from django.core.validators import RegexValidator
class Person(models.Model):    
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , null = True)#mrs 
    birth_date = models.DateField(null = True)
    country = models.CharField(max_length = 50 , null=True) 
    city = models.CharField(max_length = 50 ,null=True)   
    gender = models.BooleanField(null=True)
    bio = models.TextField(null=True)
    registration_date = models.DateField(auto_now= True , null = True)
    profile_image = models.TextField(blank=True, null=True)#helen
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))#mrs
    national_code = models.CharField(unique=True , null = True,max_length=10 , validators=[RegexValidator(r'^\d{10}$', 'Enter a valid national code.')])
    phone = models.CharField(null = True,max_length=20, validators=[
            RegexValidator(
                r'^\+?\d{1,3}[- ]?\d{3,4}[- ]?\d{4}$',
                'Enter a valid phone number.'
            )
        ])
    # def __str__(self):
        # return str(self.user_id)
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
    city_name = models.CharField(null = True, max_length=30)#this approach can't handle city name which exist in multiple country must change it to unique
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE , null = True)
    def __str__(self) -> str:
        return self.city_name

from django.core.exceptions import ValidationError#mrs
class trip_common_people(models.Model):
    trip = models.ForeignKey("Trip" , on_delete=models.CASCADE)
    common_people = models.ForeignKey(CommenPeople , on_delete=models.CASCADE)
    count = models.IntegerField(MinValueValidator(1))
    class Meta:#making fields unique can have implications for database performance and data integrity, so use this feature judiciously.
        unique_together = ('trip', 'common_people')

class Trip(models.Model):
    common_people_id = models.ManyToManyField(CommenPeople , blank = True, through="trip_common_people")
    place_ids = models.ManyToManyField(place_model.Place , blank = True)#mrs can't use null here , must use blank
    TourLeader_ids = models.ManyToManyField('TourLeader',   blank = True)#must be in same organization
    organization_id = models.ForeignKey('Organization' , on_delete=models.DO_NOTHING,null = True)
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
    image = models.TextField(null =True)
    hotel_name = models.CharField(max_length=30, null = True)

    def clean(self):#mrs
        if self.return_date and self.departure_date :
            if self.return_date < self.departure_date:
                raise ValidationError('Return date cannot be earlier than departure date.')

class Organization(models.Model):	
    person_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    name_org = models.CharField(max_length=200,unique=True , null = True)	
    description = models.TextField(null = True)	
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)# city, country	
    logo = models.TextField(blank = True, null = True)	
    Address =models.CharField(max_length=255 , null = True)	
    Phone = models.CharField(max_length=20 , null = True)	
    rates = models.IntegerField(default=0, blank=True , null = True)	
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))#mrs

    # meanrate = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
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
class PremiumRequest(models.Model):#mrs
    organization = models.ForeignKey(Organization , on_delete=models.CASCADE)
    common_people = models.ForeignKey(CommenPeople , on_delete=models.CASCADE)
    accept = 'A'
    reject = 'R'
    wait = 'W'
    STATUS_CHOICES = [

        (accept , 'accept'),

        (reject , 'reject'),

        (wait , 'wait')

    ]
    status_choice= models.CharField(max_length=1 , choices=STATUS_CHOICES , default='W')
    class Meta:#making fields unique can have implications for database performance and data integrity, so use this feature judiciously.
        unique_together = ('organization', 'common_people')

class TourLeader(models.Model):	
    person_id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)	
    orga_id = models.ForeignKey(Organization, on_delete = models.CASCADE, null= True, related_name = "tourleader")	
    rates = models.IntegerField(default=0, blank=True , null = True)	# mrs make this change to make migrations 
    rate_no = models.IntegerField(default=0, blank=True , null = True)	# mrs make this change to make migrations 
    joindDate = models.DateTimeField(auto_now=True , null = True)	# mrs make this change to make migrations 
    phonetl = models.CharField(max_length=20 , null = True)

    # meanrate = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
class Rate_Tour(models.Model):	
    tour_leader = models.ForeignKey(	
        TourLeader, on_delete=models.CASCADE, related_name='rate_tour')	
    user = models.ForeignKey(	
        User, on_delete=models.CASCADE, related_name='rates_tour')	
    rate = models.IntegerField(default=5, 	
        validators=[MinValueValidator(0), MaxValueValidator(5)])	
    def __str__(self):	
        return f"{self.user.email} rated {self.rate} to {self.tour_leader.person_id.city}"	
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

class Favorite(models.Model):
    favorite = models.TextField(null =True)
    common_people_id = models.ForeignKey(CommenPeople , on_delete=models.CASCADE)
# to send request for tourleaders that are not in an organization...
class Request(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )
    orga_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='requests')
    tl_id = models.ForeignKey(TourLeader, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('orga_id', 'tl_id')
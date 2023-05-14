from statistics import mode
from tkinter import CASCADE



from django.db import models



from django.conf import settings



from django.db import models#mrs

from Place.models import Place




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
    def __str__(self):
        return str(self.user_id)


#helen {



class CommenPeople(models.Model):



    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)



    friend_id = models.ManyToManyField("CommenPeople")
    def __str__(self) -> str:
        return str(self.Id)






class Organization(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , null = True)#mrs     
    
    name_org = models.CharField(max_length=200,unique=True)
    description = models.TextField(null = True)
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)# city, country
    # org_id = models.CharField(primary_key=True, max_length=11, unique=True)
    # tourleader_id = models.ForeignKey(TourLeader, on_delete = models.SET_NULL, null= True)
    rate = models.DecimalField(
        max_digits=2, default=0, decimal_places=1, blank=True)
    rate_no = models.IntegerField(default=0, blank=True)
    # Logo
    # logo = models.ImageField(upload_to=f'images/organs', blank=True, null=True)
    logo = models.TextField(null = True)
    Address =models.CharField(max_length=255)
    Phone = models.CharField(max_length=20)
    # Email
    # Password

    def update_rate_no(self):
        self.comment_number = self.comments.count()
        self.save()


    
    


    # (ye ghesmat bayad dashte bashe ke tour leader hash ro neshoon bede...)







class TourLeader(models.Model):



    Id = models.OneToOneField(Person, on_delete = models.CASCADE, primary_key = True)



    orga_id = models.ForeignKey(Organization, on_delete = models.SET_NULL, null= True)


    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # comment : models.TextField(max_length = 250)

    # rate = models.IntegerField(default = 0)  # in baraye khode tour leader hast..(faghat afrade sherkat konande)



class Country(models.Model):#mrs

    country_name = models.CharField(null = True , max_length=30)

    def __str__(self) -> str:

        return self.country_name





class City(models.Model):#mrs

    city_name = models.CharField(null = True, max_length=30)

    country_id = models.ForeignKey(Country, on_delete=models.CASCADE , null = True)

    def __str__(self) -> str:

        return self.city_name


class Trip(models.Model):

    place_ids = models.ManyToManyField(Place , on_delete = models.PROTECT , null = True )#, on_delete = models.PROTECT, null= True)
    TourLeader_ids = models.ManyToManyField(TourLeader, on_delete = models.DO_NOTHING ,  null = True)
    # destination_country = get from place
    # destination_city = get from place
    # origin_country = get from place
    # origin_city = get from place
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
# destinations_city
    # Transport = 
    # Departure = 
    # return = --> i dont remember it..
    # Organization_id = --> you must get it from tour leader.. 
    Description = models.TextField(null = True)
    begin_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    capacity = models.IntegerField(null = True , validators=[MinValueValidator(1)])
    

    Price = models.IntegerField(null = True , validators=[MinValueValidator(50)])
    # Place_id






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
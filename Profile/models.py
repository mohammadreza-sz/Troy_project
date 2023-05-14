from tkinter import CASCADE



from django.db import models



from django.conf import settings



from django.db import models#mrs







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



    # vali dar halate koli dar Trip ha zakhire shode bashand...



    Tour_leader_id = models.ForeignKey(TourLeader, on_delete=models.SET_NULL, null= True)



    destination_country = models.CharField(max_length=30, null = True)

    destination_city = models.CharField(max_length=30, null = True)



    origin_country = models.CharField(max_length=30, null = True)

    origin_city = models.CharField(max_length=30, null = True)



    begin_time = models.DateTimeField(null = True)



    end_time = models.DateTimeField(null = True)



    capacity = models.IntegerField(null = True)



    image = models.ImageField(upload_to = "profile/imaged" , null = True)#mrs



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
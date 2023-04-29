from distutils import text_file
from django.db import models
from Profile.models import City#mrs

# Create your models here.

class Place(models.Model):#mrs
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)
    name = models.CharField( max_length=50 ,null =True )
    address = models.CharField(max_length=250 ,null =True )
    description =models.TextField(null =True )
    lan = models.FloatField(null = True)
    lon = models.FloatField(null = True)


class PlaceImage(models.Model):#mrs
    place_id = models.ForeignKey(Place , on_delete=models.CASCADE , null = True)
    image = models.TextField(null = True)
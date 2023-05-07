from distutils import text_file

from unicodedata import name

from django.db import models

from Profile.models import City#mrs

# from Troy.settings import AUTH_USER_MODEL

from account.models import User 

from django.core.validators import MaxValueValidator, MinValueValidator





# User = AUTH_USER_MODEL

# Create your models here.



class Place(models.Model):#mrs

    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)
    # country = models.ForeignKey(country, )
    name = models.CharField( max_length=50 ,null =True )

    address = models.CharField(max_length=250 ,null =True )

    description =models.TextField(null =True )

    lan = models.FloatField(null = True)

    lon = models.FloatField(null = True)

    rate = models.DecimalField(

        max_digits=2, decimal_places=1, blank=True)

    rate_no = models.IntegerField(default=0, blank=True)

    # def update_rate(self):

    #     rates = Rate.objects.all()

    #     self.rate_no = len(rates)

    #     self.rate = round(sum(

    #         [rates.rate for rates in rates]) / self.rate_no, 1)

            # [for rate in rates.rate])/self.rate_no , 1)

        # self.rate = sum( [for i in rates.rate] ) / self.rate_no

        # self.save()

    def __str__(self) -> str:

        return self.name



class PlaceImage(models.Model):#mrs

    place_id = models.ForeignKey(Place , on_delete=models.CASCADE , null = True)

    image = models.TextField(null = True)





class Rate(models.Model):

    place = models.ForeignKey(

        Place, on_delete=models.CASCADE, related_name='rates')

    user = models.ForeignKey(

        User, on_delete=models.CASCADE, related_name='rates')

    rate = models.DecimalField(

        max_digits=2, decimal_places=1, default=5, 

        validators=[MinValueValidator(0), MaxValueValidator(5)])



    def __str__(self):

        return f"{user.name} rated {self.rate} to {self.place.name}"


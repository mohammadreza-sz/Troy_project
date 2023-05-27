from distutils import text_file

from unicodedata import name

from django.db import models

# from Profile.models import City#mrs

# from Troy.settings import AUTH_USER_MODEL

from account.models import User 

from django.core.validators import MaxValueValidator, MinValueValidator





# User = AUTH_USER_MODEL

# Create your models here.



class Place(models.Model):#mrs

    # city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)
    city_id = models.ForeignKey("Profile.City" , on_delete= models.CASCADE , null = True)
    # country = models.ForeignKey(country, )
    name = models.CharField( max_length=50 ,null =True )

    address = models.CharField(max_length=250 ,null =True )

    description =models.TextField(null =True )

    lan = models.FloatField(null = True)

    lon = models.FloatField(null = True)

    rate = models.DecimalField(

        max_digits=2, default=0, decimal_places=1, blank=True)

    rate_no = models.IntegerField(default=0, blank=True)
    comment_number = models.IntegerField(default=0)
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

    def update_rate_no(self):
        self.comment_number = self.comments.count()
        self.save()

    def update_comment_no(self):
        # self.rate_no = self.rates.count()
        self.rate_no = len(rates)
        s

import base64


class PlaceImage(models.Model):#mrs

    place_id = models.ForeignKey(Place , on_delete=models.CASCADE , null = True)
    image = models.TextField(null=True)

    # image = models.BinaryField(null = True)
    # def save_image_to_field(self, image_path):
    #     with open(image_path, "rb") as f:
    #         image_bytes = f.read()
    #         encoded_image_data = base64.b64encode(image_bytes)
    #         self.image_data = encoded_image_data

    # def get_image_as_base64(self):
    #     # return self.image_data.decode("utf-8")
    #     return self.image_data


class Rate(models.Model):

    place = models.ForeignKey(

        Place, on_delete=models.CASCADE, related_name='rates')

    user = models.ForeignKey(

        User, on_delete=models.CASCADE, related_name='rates')
    #must change to integerfield
    rate = models.DecimalField(

        max_digits=2, decimal_places=1, default=5, 

        validators=[MinValueValidator(0), MaxValueValidator(5)])



    def __str__(self):

        return f"{self.user.username} rated {self.rate} to {self.place.name}"
        # return f"rated {self.rate} to {self.place.name}"

class Comment(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, 
                        related_name='replies', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.place.title} {self.user.username}"

    def is_owner(self, user):
        return self.user == user
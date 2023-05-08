from distutils import text_file
from unicodedata import name
from django.db import models
from Profile.models import City
from account.models import User 
from django.core.validators import MaxValueValidator, MinValueValidator

class Place(models.Model):
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)
    # Image = models.
    name = models.CharField( max_length=50 ,null =True )
    like_number = models.IntegerField(default=0)
    comment_number = models.IntegerField(default=0)
    address = models.CharField(max_length=250 ,null =True )
    description =models.TextField(null =True )
    lan = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    rate = models.DecimalField(
        max_digits=2, default = 0, decimal_places=1, blank=True)
    rate_no = models.IntegerField(default=0, blank=True)
 
    def update_rate_number(self):
        self.rate_no = self.rates.count()
        self.save()

    def update_comment_number(self):
        self.comment_number = self.comments.count()
    def __str__(self) -> str:
        return self.name


class PlaceImage(models.Model):#mrs
    place_id = models.ForeignKey(Place , on_delete=models.CASCADE , null = True)
    image = models.TextField(null = True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_user')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='likes_place')
    date = models.DateField(null=True,default=None)

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
        return f"{self.place.name} {self.user.username}"

    def is_owner(self, user):
        return self.user == user


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

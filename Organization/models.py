from django.db import models
from Profile.models import Country, City
from django.contrib.auth.models import AbstractUser
from account.models import User
from unicodedata import name
from django.core.validators import MaxValueValidator, MinValueValidator

class User_org(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["email"]

class UserOrgCode(models.Model):
    user_name = models.CharField(max_length = 30)
    code = models.CharField(max_length=6)

class Organization(models.Model):
    name_org = models.CharField(max_length=200,unique=True)
    description = models.TextField(null = True)
    city_id = models.ForeignKey(City , on_delete= models.CASCADE , null = True)# city, country
    org_id = models.CharField(primary_key=True, max_length=11, unique=True)
    rate = models.DecimalField(
        max_digits=2, default=0, decimal_places=1, blank=True)
    rate_no = models.IntegerField(default=0, blank=True)
    # Logo
    Address =models.CharField(max_length=255)
    Phone = models.CharField(max_length=20)
    # Email
    # Password

    def update_rate_no(self):
        self.comment_number = self.comments.count()
        self.save()

class OrganizationImage(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE , null = True)
    image = models.TextField(null = True)

class Rate(models.Model):
    Organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='ratesOrg')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratesOrg')
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, 
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{user.name} rated {self.rate} to {self.place.name}"

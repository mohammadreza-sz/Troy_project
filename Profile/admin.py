from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Trip)
admin.site.register(Person)
admin.site.register(TourLeader)
admin.site.register(Rate_Tour)# this is for tourleader not for tours.
admin.site.register(Organization)
admin.site.register(Rate_Org)#helen
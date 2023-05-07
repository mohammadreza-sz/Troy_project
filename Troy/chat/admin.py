from django.contrib import admin

from .models import *
from account.models import User

admin.site.register(Chat)
# admin.site.register()
# you can delete them..
# admin.site.register(Contact)
# admin.site.register(Message)
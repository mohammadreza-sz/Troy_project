from django.contrib import admin

from .models import Chat

admin.site.register(Chat)

# you can delete them..
# admin.site.register(Contact)
# admin.site.register(Message)
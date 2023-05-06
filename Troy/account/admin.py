from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin#mrs #47
from .models import User#mrs#47

@admin.register(User)#mrs#47
class UserAdmin(BaseUserAdmin):#mrs#47
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2" , "email" , "first_name" , "last_name"),
            },
        ),
    )
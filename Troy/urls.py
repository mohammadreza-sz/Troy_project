from django.contrib import admin
from django.urls import path ,include
from djoser.urls import jwt
# from djoser.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('activate/', include('account.urls')),#mrs
    path('password/' , include('account.urls')),#mrs
    path('auth/', include('djoser.urls')),#mrs
    path('auth/', include('djoser.urls.jwt')),#mrs
    path('__debug__/', include('debug_toolbar.urls')),#mrs

]

from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),#mrs
    path('auth/', include('djoser.urls.jwt')),#mrs
    path('__debug__/', include('debug_toolbar.urls')),#mrs

]

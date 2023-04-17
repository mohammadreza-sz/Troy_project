from django.contrib import admin
from django.urls import path ,include



from django.conf import settings#4 mrs
from django.conf.urls.static import static#4 mrs
from djoser.urls import jwt
# from djoser.urls
urlpatterns = [

    path('admin/', admin.site.urls),

    #path('activate/', include('account.urls')),#mrs
    #path('password/' , include('account.urls')),#mrs
    path('auth/', include('djoser.urls')),#mrs

    path('auth/', include('djoser.urls.jwt')),#mrs

    path('__debug__/', include('debug_toolbar.urls')),#mrs

    path('', include('Profile.urls')),#mrs

]

if settings.DEBUG:#4 mrs
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# helen{
# from django.conf import settings
# from django.conf.urls.static import static

# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# } helen

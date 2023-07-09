from django.contrib import admin

from chat import views


from django.urls import path ,include















from django.conf import settings#4 mrs



from django.conf.urls.static import static#4 mrs



from djoser.urls import jwt



# from djoser.urls



#helen{

from rest_framework import permissions

from drf_yasg.views import get_schema_view

from drf_yasg import openapi



schema_view = get_schema_view(

   openapi.Info(

      title="Troys API",

      default_version='v1',

      description="Test description",

      terms_of_service="https://www.google.com/policies/terms/",

      contact=openapi.Contact(email="helen.azad444@gmail.com"),

      license=openapi.License(name="Test License"),

   ),

   public=True,

   permission_classes=[permissions.AllowAny],

)



urlpatterns = [







    path('admin/', admin.site.urls),





    #path('activate/', include('account.urls')),#mrs



    #path('password/' , include('account.urls')),#mrs



    path('auth/', include('djoser.urls')),#mrs





    path('auth/', include('djoser.urls.jwt')),#mrs





    path('__debug__/', include('debug_toolbar.urls')),#mrs





    path('', include('Profile.urls')),#mrs

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),#mrs

    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),#mrs

    path('account/', include('account.urls')),
    path('chat/' , include('chat.urls')),
    path('chat_room_name/' , views.CustomChat.as_view()),




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


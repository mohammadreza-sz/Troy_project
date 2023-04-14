from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),#mrs
    path('auth/', include('djoser.urls.jwt')),#mrs
    path('__debug__/', include('debug_toolbar.urls')),#mrs

]
# helen{
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# } helen
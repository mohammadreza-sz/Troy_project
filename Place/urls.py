from django.urls import path
from .views import PlaceViewSet , PlaceImageViewSet , get_specific_place , get_specific_placeimage
from rest_framework_nested import routers

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , PlaceImageViewSet)#end point => first argument without forward slash
urlpatterns = [
    path('specific_info_of_place_front' ,get_specific_place),#mrs
    path('specific_info_of_place_front/<int:place_id>' , get_specific_place),
    path('specific_info_of_place_front/<str:country_name>' ,get_specific_place),#mrs
    path('specific_info_of_place_front/<str:country_name>/<str:city_name>' ,get_specific_place),#mrs
    path('placeimage/<int:place_idd>' , get_specific_placeimage),

]
urlpatterns += router.urls#lesson 28


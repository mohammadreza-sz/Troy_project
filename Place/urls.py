from django.urls import path
from .views import PlaceViewSet , PlaceImageViewSet , get_front_info
from rest_framework_nested import routers

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , PlaceImageViewSet)#end point => first argument without forward slash

urlpatterns = [
    path('specific_info_of_place_front' ,get_front_info),#mrs
    path('specific_info_of_place_front/<int:place_id>' , get_front_info),
    path('specific_info_of_place_front/<str:country_name>' ,get_front_info),#mrs
    path('specific_info_of_place_front/<str:country_name>/<str:city_name>' ,get_front_info)#mrs
]
urlpatterns += router.urls#lesson 28


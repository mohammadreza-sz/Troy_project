from django.urls import path
from .views import PlaceViewSet , PlaceImageViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , PlaceImageViewSet)#end point => first argument without forward slash
urlpatterns = router.urls#lesson 28


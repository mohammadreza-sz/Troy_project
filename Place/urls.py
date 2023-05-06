from django.urls import path
from . import views
from rest_framework_nested import routers

app_name = 'places'

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , views.PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , views.PlaceImageViewSet)#end point => first argument without forward slash

Place_router = routers.NestedSimpleRouter(router, 'Place', lookup='Place')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 
Place_router.register('Rate',views.RateViewSet, basename='Place-Rate')#lesson 28 register child resource third ARG generating for url pattern(prefix for list and detail pattern)product-reviews-(list or detail)


urlpatterns = router.urls + Place_router.urls #lesson 28



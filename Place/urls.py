from django.urls import path

from . import views

from rest_framework_nested import routers



app_name = 'places'



router = routers.DefaultRouter()#lesson 28 two bottom line is parent router

router.register('Place' , views.PlaceViewSet)#end point => first argument without forward slash

router.register('PlaceImage' , views.PlaceImageViewSet)#end point => first argument without forward slash

urlpatterns = [

    path('specific_info_of_place_front' ,views.get_specific_place),#mrs

    path('specific_info_of_place_front/<int:place_id>' , views.get_specific_place),

    path('specific_info_of_place_front/<str:country_name>' ,views.get_specific_place),#mrs

    path('specific_info_of_place_front/<str:country_name>/<str:city_name>' ,views.get_specific_place),#mrs

    path('specific_placeimage/<int:place_idd>' , views.get_specific_placeimage),
    # path('placeimage/<int:place_idd>' , views.PlaceViewSet.as_view({"get":"g"})),
]


Place_router = routers.NestedSimpleRouter(router, 'Place', lookup='Place')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 

Place_router.register('Rate',views.RateViewSet, basename='Place-Rate')#lesson 28 register child resource third ARG generating for url pattern(prefix for list and detail pattern)product-reviews-(list or detail)





urlpatterns += router.urls + Place_router.urls #lesson 28






from django.urls import path
from django.urls import include
from . import views
from rest_framework_nested import routers

app_name = 'places'
router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , views.PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , views.PlaceImageViewSet)#end point => first argument without forward slash
Place_router = routers.NestedDefaultRouter(	
    parent_router=router, parent_prefix='Place', lookup='Place')  # place_pk	
Place_router.register('comments', views.CommentViewSet, basename='place-comments')	
comments_router = routers.NestedDefaultRouter(	
    parent_router=Place_router, parent_prefix='comments', lookup='parent')  # comment_pk	
comments_router.register('reply', views.ReplytViewSet, basename='reply')	

urlpatterns = [
    path('specific_info_of_place_front' ,views.get_specific_place),#mrs
    path('specific_info_of_place_front/<int:place_id>' , views.get_specific_place),
    path('specific_info_of_place_front/<str:country_name>' ,views.get_specific_place),#mrs
    path('specific_info_of_place_front/<str:country_name>/<str:city_name>' ,views.get_specific_place),#mrs
    path('specific_placeimage/<int:place_idd>' , views.get_specific_placeimage),
	path('plaace/', include(Place_router.urls)),	
    path('comment/', include(comments_router.urls)),

]

Place_router.register('Rate',views.RateViewSet, basename='Place-Rate')#lesson 28 register child resource third ARG generating for url pattern(prefix for list and detail pattern)product-reviews-(list or detail)
urlpatterns += router.urls + Place_router.urls #lesson 28
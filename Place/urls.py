from django.urls import path, include
# from . import views
from .views import *
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter


app_name = 'places'

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Place' , PlaceViewSet)#end point => first argument without forward slash
router.register('PlaceImage' , PlaceImageViewSet)#end point => first argument without forward slash

Place_router = routers.NestedSimpleRouter(
    router, 'Place', lookup='Place')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 
Place_router.register('Rate',RateViewSet, basename='Place-Rate')#lesson 28 register child resource third ARG generating for url pattern(prefix for list and detail pattern)product-reviews-(list or detail)

Place_router.register('comments', CommentViewSet, basename='place-comments')

comments_router = routers.NestedSimpleRouter(
    Place_router, 'comments', lookup='parent')  # comment_pk

comments_router.register('reply', ReplytViewSet, basename='reply')



# urlpatterns = router.urls + Place_router.urls #lesson 28


urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/like', LikeViewSet.as_view(), name='like-place'),
    path('<int:id>/unlike', UnLikeViewSet.as_view(), name='unlike-place'),
    # path('place/<int:placeId>', GetXpByPlace.as_view(), name='get_xp_by_place'),
    path('', include(Place_router.urls)),
    path('', include(comments_router.urls)),
]
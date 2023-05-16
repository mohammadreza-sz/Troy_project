from django.urls import path
from .views import PersonViewSet, TripViewSet , CountryViewSet , CityViewSet , FavoriteView# , s_trip
from rest_framework_nested import routers

# router = SimpleRouter()
router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Profile' , PersonViewSet)#end point => first argument without forward slash
# Person_router = routers.NestedSimpleRouter(router, 'Profile', lookup='product')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 

router.register("Trip" , TripViewSet , basename='trip')
router.register("Country" , CountryViewSet)
router.register("City" , CityViewSet)
router.register("favorite" , FavoriteView)
router.register("Person" , PersonViewSet)


# urlpatterns=[
# path("trip/" , s_trip.as_view())
# ]
urlpatterns = router.urls#lesson 28
# print(urlpatterns)
# urlpatterns = router.urls + Person_router.urls #lesson 28

    # path('users/<int:id>/', UserUpdateView.as_view()),
# print(urlpatterns)

# urlpatterns = [
#     # path('register/', UserRegisterView.as_view() , name = 'register'),
#     path('edit_profile/', PersonViewSet.as_view() , name = 'edit_profile'),

# ]
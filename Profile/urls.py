from django.urls import path
from .views import PersonViewSet, TripViewSet , CountryViewSet , CityViewSet , FavoriteView
from rest_framework_nested import routers

# router = SimpleRouter()
router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Profile' , PersonViewSet)#end point => first argument without forward slash
# Person_router = routers.NestedSimpleRouter(router, 'Profile', lookup='product')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 
router.register("Trip" , TripViewSet)
router.register("Country" , CountryViewSet)
router.register("City" , CityViewSet)
router.register("favorite" , FavoriteView)
# urlpatterns=[
    # path("favorite/me/<int:id>" , FavoriteView.as_view())
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
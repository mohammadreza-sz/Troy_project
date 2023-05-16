from django.urls import path
# from .views import PersonViewSet, TripViewSet , CountryViewSet , CityViewSet , FavoriteView
from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Profile' , PersonViewSet)#end point => first argument without forward slash
router.register("Trip" , TripViewSet)
router.register("Country" , CountryViewSet)
router.register("City" , CityViewSet)
router.register("favorite" , FavoriteView)
# router.register(prefix, viewset)

urlpatterns = [

    # (r'^ProfileInfoAPI/$', ListOrgAPIView.as_view(), name='ProfileInfoAPI'),
    # path("org/",ListOrgAPIView.as_view(),name="Org_list"),
    # path("createOrg/", CreateOrgAPIView.as_view(),name="create_Org"),
    # path("updateOrg/<int:pk>/",UpdateOrgAPIView.as_view(),name="update_Org"),
    # path("deleteOrg/<int:pk>/",DeleteOrgAPIView.as_view(),name="delete_Org"),

    # path("tl/",ListTourLeaderAPIView.as_view(),name="TourLeader_list"),
    # path("create/", CreateTourLeaderAPIView.as_view(),name="create_TourLeader"),
    # path("update/<int:pk>/",UpdateTourLeaderAPIView.as_view(),name="update_TourLeader"),
    # path("delete/<int:pk>/",DeleteTourLeaderAPIView.as_view(),name="delete_TourLeader"),
    path("TL_by_org/",get_tourleaders, name = "TL_by_org"),
    path("trip_by_org", get_toursfromOrg, name = "trip_by_org"),
    
    path("all_tourL", get_alltourleaders, name = "all_tourL"),
    path("RTL/", rate_TOURL, name = "RTL"),
]
# urlpatterns=[
    # path("favorite/me/<int:id>" , FavoriteView.as_view())
# ]

urlpatterns += router.urls#lesson 28
# print(urlpatterns)
# urlpatterns = router.urls + Person_router.urls #lesson 28

    # path('users/<int:id>/', UserUpdateView.as_view()),
# print(urlpatterns)

# urlpatterns = [
#     # path('register/', UserRegisterView.as_view() , name = 'register'),
#     path('edit_profile/', PersonViewSet.as_view() , name = 'edit_profile'),

# ]
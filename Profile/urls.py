from django.urls import path

# from .views import PersonViewSet, TripViewSet , CountryViewSet , CityViewSet , FavoriteView# , s_trip

from .views import *

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
router.register("CrudOrg" , OrganizationViewSet) #helen
router.register("CrudTourLeader", TourLeaderViewSet)#helen
router.register("Rate_org", Rate_orgViewSet, basename='Rate_org')#helen

router.register("Rate_TL",Rate_TourLViewSet, basename='Rate_TL')#helen

urlpatterns=[


path("history_user" , history_user.as_view()),
path("history_org" , history_org.as_view()),
path("history_org/<str:begindate>/<str:enddate>" , history_org.as_view()),

path("purchase" , Purchase.as_view()),

path("RequestToOrg/<int:id>" , RequestToOrg.as_view()),

path("GetRequest/" , ShowRequest.as_view()),

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

    path("list_orgs", get_orgs, name = "list_orgs"),		

    path("all_tourL", get_alltourleaders, name = "all_tourL"),		

    # path("RTL/", rate_TOURL, name = "RTL"),		

    # path("rate_Orgg/", rate_Orgg, name = "rate_Orgg"),	
    path('test' , user.as_view()),
    path('historyorg2' , histroy_org2.as_view()),
    path('passengers/<int:trip_id>' , passenger_list.as_view()),
    path('reserve' , reserve.as_view()),
    # for see the list of tourleaders that are not in a especial org
    path('organizations/<int:orga_id>/tourleaders/not-in-organization/',
         TourLeaderListNotInOrganization.as_view(), name='tourleader_not_in_organization'),

    path('requests/', RequestCreate.as_view(), name='request_create'),
    # delete a tourleader..
    path('organizations/<int:orga_id>/tourleaders/<int:tl_id>/delete/',
     TourLeaderDeleteFromOrganization.as_view(), name='tourleader_delete_from_organization'),
     path('inc_money/' , Increase_people_wallet.as_view())
]	

# path("trip/" , s_trip.as_view())

urlpatterns += router.urls 

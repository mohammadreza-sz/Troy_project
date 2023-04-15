from django.urls import path
from .views import PersonViewSet
from rest_framework_nested import routers

# router = SimpleRouter()
router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
router.register('Profile' , PersonViewSet)#end point => first argument without forward slash
urlpatterns = router.urls#lesson 28
# Person_router = routers.NestedSimpleRouter(router, 'Profile', lookup='product')#lesson 28 first ARG -> parent router second ARG -> parent prefix  third ARG -> 

# urlpatterns = router.urls + Person_router.urls #lesson 28


# print(urlpatterns)

# urlpatterns = [
#     # path('register/', UserRegisterView.as_view() , name = 'register'),
#     path('edit_profile/', PersonViewSet.as_view() , name = 'edit_profile'),

# ]
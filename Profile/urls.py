# https://codingpr.com/star-rating-blog/ --- > link of rating

from django.urls import path
from .views import TripViewSet
#rate newww
from .views import PersonViewSet
from rest_framework_nested import routers
#helen{
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Troys API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="helen.azad444@gmail.com"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    # router.urls,
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# }helen
# router = SimpleRouter()
router = routers.DefaultRouter()#lesson 28 two bottom line is parent router
# rate newww
router.register('Trip', TripViewSet)
router.register('Profile' , PersonViewSet)#end point => first argument without forward slash
# urlpatterns = router.urls + Person_router.urls #lesson 28

    # path('users/<int:id>/', UserUpdateView.as_view()),
# print(urlpatterns)

# urlpatterns = [
#     # path('register/', UserRegisterView.as_view() , name = 'register'),
#     path('edit_profile/', PersonViewSet.as_view() , name = 'edit_profile'),

# ]
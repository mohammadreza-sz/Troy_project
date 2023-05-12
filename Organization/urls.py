from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *
from django.urls import include, path

app_name = 'organization'

router = routers.DefaultRouter()
router.register('Org', OrganizationViewSet)
router.register('OrganizationImage' , views.PlaceImageViewSet)
organizations_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='', lookup='organization')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(organizations_router.urls)),
]

Organization_router.register('Rate',views.RateViewSet, basename='Organization-Rate')
urlpatterns += router.urls + ORganization_router.urls


from rest_framework.permissions import BasePermission#mrs
from rest_framework.response import Response#mrs
from rest_framework import status#mrs
class CrudOrganizationReadOther(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:            
            return bool( request.user and request.user.is_authenticated and request.user.role == "O")

class CrudAdminReadOther(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:            
            return bool( request.user and request.user.is_authenticated and request.user.is_staff)


class IsPeople(BasePermission):#mrs
    def has_permission(self , request , view):#mrs
        return bool (request.user and request.user.is_authenticated and request.user.role == "C")
    # def handle_permission_denied(self, request, message=None):#mrs
    #     # return Response({'message': message or 'Permission Denied.'}, status=status.HTTP_403_FORBIDDEN)
    #     return Response({'message': "only people can perform this action :)" }, status=status.HTTP_403_FORBIDDEN)
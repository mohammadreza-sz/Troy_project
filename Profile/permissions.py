from rest_framework.permissions import BasePermission#mrs

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
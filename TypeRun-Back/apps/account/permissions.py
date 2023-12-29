from rest_framework.permissions import BasePermission 

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email and request.user.password == obj.password or request.user.is_superuser is True

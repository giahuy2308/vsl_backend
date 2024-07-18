from rest_framework.permissions import BasePermission

class IsSuperUserOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_superuser or request.user.is_staff
    

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "POST"]:
            return True
        return request.user == obj.author
from rest_framework.permissions import BasePermission

class IsSuperUserOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_superuser
    

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "POST"]:
            return True

        try:
            return request.user == obj.author
        except AttributeError:
            return request.user == obj.administrator
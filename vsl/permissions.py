from rest_framework.permissions import IsAuthenticated

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsSuperUserOrReadOnly(IsAuthenticated):

    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.method in SAFE_METHODS or view.action == "send"):
            return True
        return request.user.is_superuser


class IsAuthor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsAuthorOrReadOnly(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return request.user == obj.user
        except AttributeError:
            try:
                return request.user == obj.administrator
            except:
                return request.user == obj.author

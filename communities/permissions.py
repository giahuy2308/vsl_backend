from rest_framework import permissions

class IsParticipantOfCommunity(permissions.BasePermission):
    """
    Custom permission to only allow participants of a community to create a page.
    """

    def has_permission(self, request, view):
        return len(request.user.communities_pa.all()) + len(request.user.communities_ad.all()) != 0

from rest_framework import permissions


class IsSameUserSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow user to edit his/her instance.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser) or (
            obj == request.user and request.method in ('PUT', 'DELETE'))


class IsOwnerSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser) or (
            obj.user == request.user and request.method in ('PUT', 'DELETE'))


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

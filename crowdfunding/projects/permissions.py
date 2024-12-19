from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows object owners to edit. Read-only for others.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsSupporterOrReadOnly(permissions.BasePermission):
    """
    Allows supporters of a pledge to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.supporter == request.user


class IsAthleteOrReadOnly(permissions.BasePermission):
    """
    Allows users with role 'athlete' or 'both' to edit their profiles.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.role in ['athlete', 'both'] and
            obj.owner == request.user
        )


class CanDonateOnly(permissions.BasePermission):
    """
    Allows users with role 'donor' or 'both' to make pledges.
    """
    def has_permission(self, request, view):
        # Allow creating pledges if user is authenticated and a donor/both
        return request.user.is_authenticated and request.user.role in ['donor', 'both']

    def has_object_permission(self, request, view, obj):
        # Donors can only view pledges, not edit them
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsBothOrFullAccess(permissions.BasePermission):
    """
    Allows users with role 'both' to perform all actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'both'

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsSupporterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow supporters of a pledge to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for SAFE_METHODS (GET, HEAD, OPTIONS).
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only allowed to the supporter of the pledge.
        return obj.supporter == request.user

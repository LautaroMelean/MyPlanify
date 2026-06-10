from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    """Allow access only to the resource owner or an admin."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == "admin"


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")

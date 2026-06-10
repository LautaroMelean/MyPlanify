from rest_framework.permissions import BasePermission, SAFE_METHODS


class EventPermission(BasePermission):
    """Read: public. Write: event_organizer or admin."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ("admin", "event_organizer", "moderator")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role in ("admin", "moderator"):
            return True
        return obj.organizer == request.user

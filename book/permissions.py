from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_staff:
            return False
        return True

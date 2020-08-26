from rest_framework import permissions

from api.models import UserRole


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    (request.user.is_staff or request.user.role == UserRole.ADMIN)
                    )


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    (request.user.is_staff or
                     request.user.role == UserRole.ADMIN) or
                    request.method in permissions.SAFE_METHODS)


class ReviewOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS or
                    obj.author == request.user or
                    request.user.role == UserRole.MODERATOR)

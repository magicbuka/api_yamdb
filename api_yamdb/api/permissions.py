from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Полный доступ только для администратора или суперпользователя
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin()
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    POST, PATCH, DEL - admin, superuser
    GET, HEAD, OPTIONS - все пользователи
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin()
        return request.method in permissions.SAFE_METHODS


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """
    GET, HEAD, OPTIONS - все пользователи
    POST, PATCH, DEL - автор, moderator, admin, superuser
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_moderator()
                or request.user.is_admin()
            )
        return request.method in permissions.SAFE_METHODS

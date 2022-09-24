from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Полный доступ только для администратора или суперпользователя
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    POST, PATCH, DEL - admin, superuser
    GET, HEAD, OPTIONS - все пользователи
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin()
            )
        )


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """
    GET, HEAD, OPTIONS - все пользователи
    POST, PATCH, DEL - автор, moderator, admin, superuser
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or (
                request.user.is_authenticated and (
                    request.user.is_moderator()
                    or request.user.is_admin()
                )
            )
        )

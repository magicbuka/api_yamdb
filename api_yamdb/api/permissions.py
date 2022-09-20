from rest_framework import permissions


class OwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Изменение доступно только автору контента, читать может любой
    """
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or (request.method in permissions.SAFE_METHODS)
                or request.user.role == 'admin' or request.user.is_superuser
                )


class IsAdmin(permissions.BasePermission):
    """
    Полный доступ только для администратора или суперпользователя
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS 
            or (
                request.user.is_authenticated 
                and request.user.role == 'admin'
            )
        )


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS 
            or (
                obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
            )
        )

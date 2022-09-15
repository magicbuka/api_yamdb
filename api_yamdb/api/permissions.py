from rest_framework import permissions


class OwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or
                (request.method in permissions.SAFE_METHODS) or
                request.user.role == 'a' or request.user.is_superuser
                )

from rest_framework import permissions

from .exceptions import GenericAPIException
from .models import Follow


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class FollowNotExistsAndCantFollowYourself(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.username == request.data.get('following'):
                raise GenericAPIException(
                    detail='Can not follow yorself'
                )
            elif Follow.objects.filter(
                user=request.user,
                following__username=request.data.get('following')
            ).exists():
                raise GenericAPIException(
                    detail='Follow object has already exist'
                )
        return True

from rest_framework.permissions import BasePermission

from accounts.utils import user_without_team


class UserWithoutTeam(BasePermission):

    def has_permission(self, request, view):
        return user_without_team(request.user)
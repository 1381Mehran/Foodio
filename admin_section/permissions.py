from rest_framework import permissions
from .models import Admin, Staff


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return False


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if Admin.objects.filter(user=request.user).exists() or Staff.objects.filter(user=request.user).exists():
            return True

        return False


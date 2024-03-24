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


class IsSupportAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if Admin.objects.filter(position='support', user=request.user, is_active=True).exists():
            return True
        return False


class IsFinancialAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if Admin.objects.filter(position='financial', user=request.user, is_active=True).exists():
            return True
        return False


class IsProductAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if Admin.objects.filter(position='product', user=request.user, is_active=True).exists():
            return True
        return False


class IsTechnicalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if Admin.objects.filter(position='technical', user=request.user, is_active=True).exists():
            return True
        return False


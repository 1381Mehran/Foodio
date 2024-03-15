from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission, SAFE_METHODS

from admin_section.models import Admin, Staff


class IsCatAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if ((request.method in SAFE_METHODS) or
           Admin.objects.filter(position='product', user=request.user).exists() or
           Staff.objects.filter(position='product', user=request.user).exists()):

            return True

        elif get_user_model().objects.filter(id=request.user.id, is_superuser=True).exists():
            return True

        else:
            return False



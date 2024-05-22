from rest_framework.permissions import BasePermission
from seller.models import Seller


class IsSeller(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return obj.is_active
        return False


class IsAuthenticateSeller(BasePermission):

    def has_permission(self, request, view):
        if Seller.objects.filter(user=request.user).exists():
            return request.user.seller.is_active

        return False


class IsSellerProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.seller == request.user:
            return obj.seller.is_active
        return False


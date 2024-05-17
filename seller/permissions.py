from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return obj.is_active
        return False


class IsSellerProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.seller == request.user:
            return obj.seller.is_active
        return False


from enum import Enum, unique

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from extensions.tools import category_schema
from admin_section.models import Admin
from account.utils import Authentication
from seller.models import Seller
from product.api.serializers import AddEditCatSerializer


class SellerSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    phone = serializers.SerializerMethodField()
    work_class = serializers.CharField(max_length=250)
    work_class_number = serializers.CharField(max_length=30)
    state = serializers.SerializerMethodField()
    address = serializers.CharField(max_length=300)
    is_active = serializers.BooleanField()

    def get_state(self, obj):
        return {
            'id': obj.state.id,
            'title': obj.state.title,
            'parent': {
                'id': obj.state.parent.id,
                'title': obj.state.parent.title
            }
        }

    def get_phone(self, obj):
        return obj.user.phone

    class Meta:
        ref_name = 'admin-section'


class AcceptingSellerSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get('is_active') is False and attrs.get('not_confirmed_cause') is None:
            raise ValidationError('not_confirmed_cause is required')

        return attrs

    class Meta:
        model = Seller
        fields = ('is_active', 'not_confirmed_cause')
        extra_kwargs = {
            'not_confirmed_cause': {'required': False}
        }
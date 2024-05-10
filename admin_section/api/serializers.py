from enum import Enum, unique

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from extensions.tools import category_schema
from product.models import MainCat
from ..models import Admin
from account.utils import Authentication
from seller.models import Seller


class ImprovePositionSerializer(serializers.Serializer):
    user_phone = serializers.CharField(
        max_length=10, min_length=10
    )

    admin_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    level = serializers.CharField(max_length=5)

    position = serializers.CharField(max_length=10)

    password = serializers.CharField(
        min_length=8,
        allow_blank=True,
        allow_null=True,
        required=False
    )

    def validate_user_phone(self, obj):
        if not get_user_model().objects.filter(phone=obj).exists():
            raise ValidationError('User with phone {0} not found !...'.format(obj))

        return obj

    def validate_admin_id(self, obj):
        if not Admin.objects.filter(id=obj).exists():
            raise ValidationError('Admin with ID {0} not found !...'.format(obj))

        return int(obj)

    def validate_level(self, obj):
        @unique
        class Levels(Enum):
            ADMIN = 'admin'
            STAFF = 'staff'

        if not (obj == Levels.ADMIN.value or obj == Levels.STAFF.value):
            raise ValidationError('Invalid level')

        return obj

    def validate_position(self, obj):

        @unique
        class Positions(Enum):
            FINANCIAL = 'financial'
            TECHNICAL = 'technical'
            SUPPORT = 'support'
            PRODUCT = 'product'

        if not (obj == Positions.FINANCIAL.value or obj == Positions.TECHNICAL.value or
                obj == Positions.SUPPORT.value or obj == Positions.PRODUCT.value):
            raise ValidationError('Invalid position')

        return obj

    def validate_password(self, obj):

        status, errors = Authentication.check_password_format(obj)

        if not status:
            raise ValidationError(errors)

        return obj

    def validate(self, attrs):
        if attrs.get('level') == 'staff' and 'admin_id' not in attrs:
            raise ValidationError('admin field is required for staff level')

        return attrs


class ChangeAdminOrStaffPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100, min_length=8)
    new_password = serializers.CharField(max_length=100, min_length=8)

    def validate_old_password(self, obj):
        request = self.context.get('request')

        status = check_password(obj, request.user.password)

        if not status:
            raise ValidationError('old password is incorrect')

        return obj

    def validate_new_password(self, obj):
        status, errors = Authentication.check_password_format(obj)

        if not status:
            raise ValidationError(errors)

        return obj


# Relating to Sellers

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

# Relating to Acceptance Categories


class CategorySerializer(serializers.Serializer):

    title = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
        write_only=True
    )
    active = serializers.BooleanField(
        required=False,
        write_only=True
    )

    cat_type = serializers.CharField(max_length=7, write_only=True)

    def validate_cat_type(self, value):
        if value.lower() not in ['main_cat', 'mid_cat', 'sub_cat']:
            raise ValidationError('active is invalid')

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['main_cat'] = {}
        representation['mid_cat'] = {}
        representation['sub_cat'] = {}

        class CatType(Enum):
            MAIN = 'main_cat'
            MID = 'mid_cat'
            SUB = 'sub_cat'

        def insert_cat(type_): return representation[type_].update({
                    'id': instance.id,
                    'title': instance.title,
                    'active': instance.is_active,
                })

        match instance.type:
            case CatType.MAIN.value:
                insert_cat(CatType.MAIN.value)

            case CatType.MID.value:
                insert_cat(CatType.MID.value)

            case CatType.SUB.value:
                insert_cat(CatType.SUB.value)

        return representation


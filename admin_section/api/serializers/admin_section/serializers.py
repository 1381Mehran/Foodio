from enum import Enum, unique

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from admin_section.models import Admin
from account.utils import Authentication


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
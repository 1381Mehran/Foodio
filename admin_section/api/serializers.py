from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from enum import Enum, unique

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models import Admin


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
        if not any(True if char in ascii_lowercase else False for char in obj):
            raise ValidationError('password must contain at least one lowercase')

        if not any(True if _ in ascii_uppercase else False for _ in obj):
            raise ValidationError('password must contain at least one UpperCase')

        if not any(True if _ in digits else False for _ in obj):
            raise ValidationError('password must contain at least one digits')

        if not any(True if _ in punctuation else False for _ in obj):
            raise ValidationError('password must contain at least one Symbol')

        return obj

    def validate(self, attrs):
        if attrs.get('level') == 'staff' and 'admin' not in attrs:
            raise ValidationError('admin field is required for staff level')

        return attrs

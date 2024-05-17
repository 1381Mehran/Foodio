from enum import Enum, unique

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from extensions.tools import category_schema
from product.models import MainCat, MidCat, SubCat
from ..models import Admin
from account.utils import Authentication
from seller.models import Seller
from product.api.serializers import AddEditCatSerializer


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

    type = serializers.CharField(max_length=8, write_only=True)

    def validate_type(self, value):
        if value.lower() not in ['main_cat', 'mid_cat', 'sub_cat']:
            raise ValidationError(f'{value} is invalid')

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # representation['main_cat'] = {}
        # representation['mid_cat'] = {}
        # representation['sub_cat'] = {}

        class CatType(Enum):
            MAIN = 'main_cat'
            MID = 'mid_cat'
            SUB = 'sub_cat'

        match instance.type:
            case CatType.MAIN.value:
                representation.update(category_schema(instance))

            case CatType.MID.value:
                representation.update(category_schema(instance))

            case CatType.SUB.value:
                representation.update(category_schema(instance))

        return representation


class AdminAddEditCatSerializer(AddEditCatSerializer):

    """
    field_tips:
        active: this field in db is "is_active" but I change name field for more security
    """

    active = serializers.BooleanField()

    def create(self, validated_data):
        @unique
        class CatType(Enum):
            MAIN_CAT = 'main_cat'
            MID_CAT = 'mid_cat'
            SUB_CAT = 'sub_cat'

        match validated_data['type']:
            case CatType.MAIN_CAT.value:
                if not MainCat.objects.filter(title=validated_data['title']).exists():
                    return MainCat.objects.create(
                        title=validated_data['title'],
                        is_active=validated_data['active'],
                    )
                else:
                    raise ValidationError({'error': 'category is duplicated'})

            case CatType.MID_CAT.value:
                if not MidCat.objects.filter(title=validated_data['title']).exists():

                    return MidCat.objects.create(
                        title=validated_data['title'],
                        parent_id=validated_data.get('parent_id'),
                        is_active=validated_data['active'],
                    )
                else:
                    raise ValidationError({'error': 'category is duplicated'})

            case CatType.SUB_CAT.value:
                if not SubCat.objects.filter(title=validated_data['title']).exists():
                    return SubCat.objects.create(
                        title=validated_data['title'],
                        parent_id=validated_data.get('parent_id'),
                        is_active=validated_data['active'],
                    )
                else:
                    raise ValidationError({'error': 'category is duplicated'})

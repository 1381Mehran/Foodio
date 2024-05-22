from rest_framework import serializers
from rest_framework.serializers import ValidationError

from product.api.serializers import GetCatSerializer
from product.models import Product, ProductCategory, ProductImage, ProductProperty
from ..models import State, Seller
from admin_section.api.serializers import ChangeAdminOrStaffPasswordSerializer
from extensions.custom_serializer_fields import AbsoluteURLImageField


##############################################################
#                    Seller Serializers                      #
##############################################################


class RetrieveStateSerializer(serializers.Serializer):

    def to_representation(self, instance):
        representation = super(RetrieveStateSerializer, self).to_representation(instance)

        if not instance.parent and instance.type == 'state':
            representation['state'] = {
                'id': instance.id,
                'title': instance.title,
            }

            children = instance.children.filter(is_active=True, type='city')

            if children.count() > 1:

                representation['cities'] = [{'id': item.id, 'title': item.title} for item in children]

            else:
                if children:
                    representation['cities'] = {'id': children[0].id, 'title': children[0].title}
                else:
                    representation['cities'] = None
        else:
            representation['state'] = {'id': instance.parent.id, 'title': instance.parent.title}
            representation['cities'] = {'id': instance.id, 'title': instance.title}

        return representation


class CreateAndUpdateStateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=State.objects.filter(type='state'), required=False)

    def validate(self, attrs):
        if attrs.get('type') == 'city':
            if not attrs.get('parent'):
                raise ValidationError('parent is required')

        return attrs

    class Meta:
        model = State
        fields = ('title', 'type', 'parent')
        extra_kwargs = {
            'type': {'required': True}
        }

    # def validate_type(self, obj):
    #     if obj not in ['city', 'state']:
    #         raise ValidationError('invalid type')
    #
    #     return obj


class SellerSerializer(serializers.ModelSerializer):

    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.filter(
        is_active=True, type='city', parent__isnull=False), write_only=True)

    city = serializers.SlugRelatedField(slug_field='title', read_only=True, source='state')

    class Meta:
        model = Seller
        fields = ('work_class', 'work_class_number', 'state', 'city', 'address', 'is_active')
        read_only_fields = ('is_active', 'city')
        write_only_fields = ('state',)
        ref_name = 'Seller'


class ChangeSellerPasswordSerializer(ChangeAdminOrStaffPasswordSerializer):
    pass


##############################################################
#                   Product Serializers                      #
##############################################################


class ProductImagesSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    image = AbsoluteURLImageField()

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'type', 'image')
        read_only_fields = ('id',)
        write_only_fields = ('product',)


class ProductPropertySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    item_type = serializers.ChoiceField(choices=ProductProperty.PropertyType.choices)

    class Meta:
        model = ProductProperty
        fields = ('id', 'product', 'item_type', 'item_name', 'item_detail')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.filter(
        is_active=True,
        parent__isnull=False,
        parent__parent__isnull=False,
    ), write_only=True)

    product_properties = ProductPropertySerializer(many=True, read_only=True)

    product_images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'introduce', 'category', 'stock', 'is_active')
        read_only_fields = ('id', 'is_active')

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)

        representation.update({'categories': GetCatSerializer(instance=instance.category).data})

        return representation


# class RetrieveProductSerializer(serializers.Serializer):
#     id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#     category = serializers.SerializerMethodField()
#     title = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#     introduce = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#     properties = serializers.SerializerMethodField()
#     images = serializers.SerializerMethodField()
#     is_active = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#
#     def get_category(self, obj):
#         return GetCatSerializer(instance=obj.category, many=True).data
#
#     def get_properties(self, obj):
#         return [{'item_type': prop.item_type, 'item_name': prop.item_name, 'item_detail': prop.item_detail}
#                 for prop in obj.product_properties.filter(is_active=True)]
#
#     def get_images(self, obj):
#
#         request = self.context.get('request', None)
#
#         return [{'type': img.item_type, "url": request.build_absolute_uri(img.image.url) if request else None}
#                 for img in obj.product_images.filter(is_active=True)]


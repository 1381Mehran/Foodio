from rest_framework import serializers

from extensions.custom_serializer_fields import AbsoluteURLImageField
from product.models import Product, ProductImage, ProductProperty, ProductCategory
from product.api.serializers import GetCatSerializer


class ProductImagesSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(read_only=True)
    image = AbsoluteURLImageField()

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'type', 'image')
        read_only_fields = ('id',)
        write_only_fields = ('product',)
        extra_kwargs = {
            'product': {'required': True},
            'type': {'required': True},
            'image': {'required': True},
        }

    def to_representation(self, instance):
        representation = super(ProductImagesSerializer, self).to_representation(instance)

        self.fields['product'].queryset = Product.objects.filter(seller__user_id=self.context.get('request').user.id)

        return representation


class ProductPropertySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    item_type = serializers.ChoiceField(choices=ProductProperty.PropertyType.choices)

    class Meta:
        model = ProductProperty
        fields = ('id', 'product', 'item_type', 'item_name', 'item_detail')
        read_only_fields = ('id',)
        extra_kwargs = {
            'product': {'required': True},
            'item_type': {'required': True},
            'item_name': {'required': True},
            'item_detail': {'required': True},
        }


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
        fields = ('id', 'title', 'introduce', 'category', 'stock', 'product_type', 'is_active')
        read_only_fields = ('id', 'product_type', 'is_active')

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)

        representation.update({'categories': GetCatSerializer(instance=instance.category).data})

        return representation


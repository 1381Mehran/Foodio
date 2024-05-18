from django.db.models import Q

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models import Product, ProductCategory
from extensions.tools import category_schema


class GetCatSerializer(serializers.Serializer):

    def to_representation(self, instance):
        representation = super(GetCatSerializer, self).to_representation(instance)

        # type_ = self.context.get('type', None)
        #
        # @unique
        # class CatType(Enum):
        #     MAIN_CAT = 'main_cat'
        #     MID_CAT = 'mid_cat'
        #     SUB_CAT = 'sub_cat'
        #
        # match type_:
        #     case CatType.MAIN_CAT.value:
        #         representation['main_cat'] = instance.title
        #         representation['mid_cat'] = instance.mid_cats.filter(active=True).value_list('title', flat=True)
        #         representation['sub_cat'] = [cat.sub_cats.filter(active=True).title for cat in instance.mid_cats
        #                                      if cat.sub_cats.filter(active=True).title not in representation['sub_cat']]
        #
        #     case CatType.MID_CAT.value:
        #         representation['mid_cat'] = instance.title
        #         representation['main_cat'] = instance.main_cat.title
        #         representation['sub_cat'] = instance.sub_cat.filter(active=True).title
        #
        #     case CatType.SUB_CAT.value:
        #         representation['sub_cat'] = instance.title
        #         representation['mid_cat'] = instance.parent.title
        #         representation['main_cat'] = instance.parent.parent.title

        representation.update(category_schema(instance))

        return representation


class AddEditCatSerializer(serializers.Serializer):
    # type = serializers.CharField()
    title = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.filter(is_active=True),
        required=False
    )

    def validate_title(self, value):
        if ProductCategory.objects.filter(
                Q(title__exact=value) |
                Q(parent__title__exact=value) |
                Q(parent__parent__title__exact=value)
        ).exists():
            raise ValidationError("Title already exists")

        return value

    # def validate_type(self, value):
    #     authorized_types = ['main_cat', 'mid_cat', 'sub_cat']
    #     if value not in authorized_types:
    #         raise ValidationError('type is invalid')
    #
    #     return value

    def create(self, validated_data):

        # @unique
        # class CatType(Enum):
        #     MAIN_CAT = 'main_cat'
        #     MID_CAT = 'mid_cat'
        #     SUB_CAT = 'sub_cat'

        # match validated_data['type']:
        #     case CatType.MAIN_CAT.value:
        #         if not MainCat.objects.filter(title=validated_data['title']).exists():
        #             return MainCat.objects.create(title=validated_data['title'])
        #         else:
        #             raise ValidationError({'error': 'category is duplicated'})
        #
        #     case CatType.MID_CAT.value:
        #         if not MidCat.objects.filter(title=validated_data['title']).exists():
        #
        #             return MidCat.objects.create(
        #                 title=validated_data['title'],
        #                 parent_id=validated_data.get('parent_id')
        #             )
        #         else:
        #             raise ValidationError({'error': 'category is duplicated'})
        #
        #     case CatType.SUB_CAT.value:
        #         if not SubCat.objects.filter(title=validated_data['title']).exists():
        #             return SubCat.objects.create(
        #                 title=validated_data['title'],
        #                 parent_id=validated_data.get('parent_id')
        #             )
        #         else:
        #             raise ValidationError({'error': 'category is duplicated'})

        return ProductCategory.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.save()
    #     return instance



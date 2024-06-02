from rest_framework import serializers

from extensions.tools import category_schema
from product.api.serializers import AddEditCatSerializer


class CategorySerializer(serializers.Serializer):

    # title = serializers.CharField(
    #     max_length=100,
    #     required=False,
    #     allow_blank=True,
    #     allow_null=True,
    #     write_only=True
    # )
    # active = serializers.BooleanField(
    #     required=False,
    #     write_only=True
    # )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.update(category_schema(instance))

        return representation


class AdminAddEditCatSerializer(AddEditCatSerializer):

    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save(update_fields=[key])

        return instance


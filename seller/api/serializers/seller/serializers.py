from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ....models import State, Seller
from admin_section.api.serializers import ChangeAdminOrStaffPasswordSerializer


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

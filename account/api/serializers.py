from rest_framework import serializers
from rest_framework.serializers import ValidationError

from account.models import CardNumber
from extensions.custom_serializer_fields import AbsoluteURLImageField


class AuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=10,
        min_length=10
    )
    password = serializers.CharField(
        min_length=8,
        max_length=20,
        allow_null=True,
        allow_blank=True,
        required=False
    )
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        allow_blank=True,
        required=False,
        allow_null=True
    )


class UserProfileSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    national_id = serializers.CharField(min_length=10, max_length=10)
    image = AbsoluteURLImageField()
    card_numbers = serializers.SerializerMethodField(read_only=True)

    # def get_image(self, obj):
    #     request = self.context.get('request')
    #
    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)

    def get_card_numbers(self, instance):
        return [{'card_number': card.card_number, 'sheba_number': card.sheba_number}
                for card in instance.card_numbers.all()]

    # def to_representation(self, instance):
    #     representation = super(UserProfileSerializer, self).to_representation(instance)
    #
    #     representation['card_numbers'] = [{'card_number': card.card_number, 'sheba_number': card.sheba_number}
    #                                       for card in instance.card_numbers.all()]
    #
    #     return representation

    def validate(self, attrs):
        if len(attrs) == 0:
            raise ValidationError('you must choice at least a field')

        return attrs


class UserCardNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardNumber
        fields = ('id', 'card_number', 'sheba_number', 'is_active')
        extra_kwargs = {'id': {'read_only': True}}
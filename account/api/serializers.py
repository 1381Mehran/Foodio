from rest_framework import serializers


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


from django.db import models

from rest_framework import serializers


class AbsoluteURLImageField(serializers.ImageField):

    """
    Serializer field to return the image url as an absolute URI.
    """

    def to_representation(self, value):
        request = self.context.get('request')

        if request is not None:
            if isinstance(value, models.Model):
                return request.build_absolute_uri(value.uri)
            else:
                return super(AbsoluteURLImageField, self).to_representation(value)
        else:
            return super(AbsoluteURLImageField, self).to_representation(value)


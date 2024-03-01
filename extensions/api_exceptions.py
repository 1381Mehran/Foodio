from rest_framework.exceptions import APIException


class SerializerException(APIException):
    status_code = 400
    default_detail = {'metadata': []}

    def __init__(self, serializer_errors=None, *args, **kwargs):
        if serializer_errors:
            self.default_detail['metadata'] = serializer_errors
        super(SerializerException, self).__init__(self.default_detail, **kwargs)

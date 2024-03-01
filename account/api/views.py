from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from extensions.renderers import CustomJSONRenderer
from ..utils import Authentication
from .serializers import AuthenticationSerializer
from extensions.api_exceptions import SerializerException


class LoginView(APIView):
    serializer_class = AuthenticationSerializer
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        authentication = Authentication()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data.get('phone')
            password = serializer.data.get('password')

            result = authentication.login(phone, password)

            if isinstance(result, int):
                return Response({"otp": result})
            else:
                return Response({'error': result}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise SerializerException(serializer.errors)



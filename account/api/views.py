from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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

            if len(result) == 6:
                return Response({"otp": f"{result}"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise SerializerException(serializer.errors)


class VerifyView(APIView):
    renderer_classes = [CustomJSONRenderer]
    serializer_class = AuthenticationSerializer

    def post(self, request):
        authentication = Authentication()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')
            code = serializer.data.get('code')

            result, status_ = authentication.verify(phone, code)

            if isinstance(result, dict):
                if status_:
                    return Response(result, status.HTTP_201_CREATED)
                else:
                    return Response(result)

            else:
                return Response({'error': result}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise SerializerException(serializer.errors)


class LogoutView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        authentication = Authentication()
        result, status_ = authentication.logout(request)

        if status_:

            return Response({"message": result}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': result}, status=status.HTTP_403_FORBIDDEN)



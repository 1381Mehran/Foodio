from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from extensions.renderers import CustomJSONRenderer
from ..models import CardNumber
from ..utils import Authentication
from .serializers import AuthenticationSerializer, UserProfileSerializer, UserCardNumberSerializer
from extensions.api_exceptions import SerializerException


class LoginView(APIView):

    """
    POST:
        : login to site for jwt token

        parameters: 1- phone(required), 2- password(Just for sellers or admins is required)

    """

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

    """
    POST:
        : verify user by phone number and OTP code

        parameters: 1- phone(required), 2- code(required)
    """

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

    """
    POST:
        : logout user
    """


    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        authentication = Authentication()
        result, status_ = authentication.logout(request)

        if status_:

            return Response({"message": result}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': result}, status=status.HTTP_403_FORBIDDEN)


class UserProfileView(APIView):

    """
    GET:
        : get user profile

    PUT:
        : update user profile
        parameters: 'first_name', 'last_name', 'email', 'national_id', 'image'


    DELETE:
          : delete user account

    """

    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.user, partial=True)
        if serializer.is_valid():
            for field in ['first_name', 'last_name', 'email', 'national_id', 'image']:
                if serializer.validated_data.get(field, None):
                    setattr(request.user, field, serializer.validated_data.get(field))
                    request.user.save(update_fields=[field])

            return Response({'success': True}, status.HTTP_202_ACCEPTED)

        else:
            raise SerializerException(serializer.errors)

    def delete(self, request):
        request.user.delete()
        return Response({'success': True}, status.HTTP_204_NO_CONTENT)


class UserCardNumberView(APIView):

    """
    GET:
        : Get user card number list

    POST:
         : Create user card number

         body => 1- card_number(required), 2- sheba_number(optional)

    PUT:
         : update user card number
         body => 1- card_number, 2- sheba_number, 3- is_active

    DELETE:
            : Delete user card number
            kwargs => pk -> card_number instance_id
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = UserCardNumberSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user.card_numbers.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'success': True}, status.HTTP_201_CREATED)
        else:
            raise SerializerException(serializer.errors)

    def put(self, request, pk):
        try:
            instance = request.user.card_numbers.get(id=pk)
        except CardNumber.DoesNotExist:
            return Response({'error': 'CardNumber does not found'}, status=404)
        else:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True}, status.HTTP_202_ACCEPTED)
            else:
                raise SerializerException(serializer.errors)

    def delete(self, request, pk):
        try:
            instance = request.user.card_numbers.get(id=pk)
        except CardNumber.DoesNotExist:
            return Response({'error': 'CardNumber does not found'}, status=404)
        else:
            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)



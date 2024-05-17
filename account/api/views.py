from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from extensions.renderers import CustomJSONRenderer
from extensions.send_mail import SendMailThread
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

    @swagger_auto_schema(
        operation_summary="login",
        operation_description="get OTP code to login to site",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    minLength=10,
                    maxLength=10,
                    description='Phone number',
                    example='9371111111'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    minLength=8,
                    maxLength=20,
                    description='Enter your password',
                    example='<PASSWORD>'
                )
            },
            required=['phone']
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_STRING)
                },
                description='get OTP code to login to'
            ),
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_STRING)
                },
                description='get OTP code to login'
            ),
            status.HTTP_406_NOT_ACCEPTABLE: "Invalid phone or password",
            status.HTTP_400_BAD_REQUEST: "Serializer Problem"
        }

    )
    def post(self, request):
        authentication = Authentication()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data.get('phone')
            password = serializer.data.get('password')

            result = authentication.login(phone, password)

            if isinstance(result, str) and result.isnumeric():
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

    @swagger_auto_schema(
        operation_summary="Verify",
        operation_description='get refresh token and access token',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    minLength=10,
                    maxLength=10,
                    description='Phone number',
                    example='9371111111'
                ),
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    minLength=6,
                    maxLength=6,
                    description='OTP code',
                    example='<OTP CODE>'
                )
            },
            required=['phone', 'code']
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            status.HTTP_400_BAD_REQUEST: 'problem'
        }
    )
    def post(self, request, *args, **kwargs):
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

                    if (get_user_model().objects.filter(phone=phone).exists() and
                            get_user_model().objects.get(phone=phone).email):

                        SendMailThread(
                            'شرکت جاوید',
                            f'کد ورود شما : {result}',
                            [get_user_model().objects.get(phone=phone).email],
                        ).start()

                    return Response(result)

            else:
                return Response({'error': result}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise SerializerException(serializer.errors)


class LogoutView(APIView):

    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="logout",
        operation_description="logout user",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'massage': openapi.Schema(type=openapi.TYPE_STRING)},
            ),
            status.HTTP_403_FORBIDDEN:openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):

        authentication = Authentication()
        result, status_ = authentication.logout(request)

        if status_:

            return Response({"message": result}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': result}, status=status.HTTP_403_FORBIDDEN)


class UserProfileView(APIView):

    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_summary="profile_info",
        operation_description="get user profile information",
        responses={
            status.HTTP_200_OK: UserProfileSerializer(),
        },
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="profile_edit",
        operation_description="edit user profile",
        request_body=UserProfileSerializer,
        responses={
            status.HTTP_200_OK: '{"success": True}',
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        }
    )
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=request.user, partial=True)
        if serializer.is_valid():
            for field in ['first_name', 'last_name', 'email', 'national_id', 'image']:
                if serializer.validated_data.get(field, None):
                    setattr(request.user, field, serializer.validated_data.get(field))
                    request.user.save(update_fields=[field])

            return Response({'success': True}, status.HTTP_202_ACCEPTED)

        else:
            raise SerializerException(serializer.errors)

    @swagger_auto_schema(
        operation_summary="profile_delete",
        operation_description="delete user Account - just must be authenticated",
        responses={
            status.HTTP_204_NO_CONTENT: '{"success": True}',
        }
    )
    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({'success': True}, status.HTTP_204_NO_CONTENT)


class UserCardNumberView(APIView):

    """
        get:
             Get user card number list

        post:
              Create user card number

             request_body = {card_number: string, sheba_number: string}
             required = ['card_number']
             response_body

        put:
             update user card number
             request_body = {card_number: string, sheba_number: string, is_active: boolean}
             required = ['card_number', 'sheba_number']


        delete:
                : Delete user card number
                kwargs => pk -> card_number instance_id
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = UserCardNumberSerializer

    @swagger_auto_schema(
        operation_summary='user card number',
        operation_description='get user card number',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='dont enter id in this webservice',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: UserCardNumberSerializer(many=True)
        },
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user.card_numbers.all(),
            many=True
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'success': True}, status.HTTP_201_CREATED)
        else:
            raise SerializerException(serializer.errors)

    def put(self, request, pk, *args, **kwargs):
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

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = request.user.card_numbers.get(id=pk)
        except CardNumber.DoesNotExist:
            return Response({'error': 'CardNumber does not found'}, status=404)
        else:
            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)



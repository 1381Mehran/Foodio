from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from extensions.renderers import CustomJSONRenderer
from ..permissions import IsSuperUser, IsAdminOrStaff
from ..models import Admin, Staff
from account.utils import Authentication
from extensions.api_exceptions import SerializerException


class ImprovePositionView(CreateAPIView):
    serializer_class = ImprovePositionSerializer
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_phone = serializer.data.get('user_phone')
            admin_id = serializer.data.get('admin_id', None)
            level = serializer.data.get('level')
            position = serializer.data.get('position')
            password = serializer.data.get('password')

            @unique
            class Levels(Enum):
                ADMIN = 'admin'
                STAFF = 'staff'

            user = get_user_model().objects.get(phone=user_phone)

            if (user.national_id and
                    user.image and
                    (user.card_numbers.filter(is_active=True).count() > 0) and
                    user.first_name and user.last_name):

                if not password:
                    password = Authentication().password_generator

                match level:

                    case Levels.ADMIN.value:

                        try:
                            Admin.objects.create(user=user, position=position)

                        except IntegrityError:
                            return Response({'error': 'User with level admin already exists'},
                                            status.HTTP_403_FORBIDDEN)

                        else:
                            user.password = password
                            user.save(update_fields=['password'])

                            return Response({'phone': user_phone, 'password': password},
                                            status=status.HTTP_201_CREATED)

                    case Levels.STAFF.value:

                        admin = Admin.objects.get(id=admin_id)

                        user.password = password
                        user.save(update_fields=['password'])

                        if not Staff.objects.filter(phone=user_phone).exists():
                            Staff.objects.create(user=user, position=position, admin=admin)
                        else:
                            return Response({'error': 'User with level "admin" already exists'},
                                            status.HTTP_403_FORBIDDEN)

                        return Response({'phone': user_phone, 'password': password}, status.HTTP_201_CREATED)

            else:
                return Response({'error': "national_id, image, first_name and last_name are required and card_number have to be more than one"},
                                status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise SerializerException(serializer.errors)


class ChangeAdminOrStaffPasswordView(UpdateAPIView):
    permission_classes = [IsAdminOrStaff]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = ChangeAdminOrStaffPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            new_password = serializer.data.get('new_password')

            user = get_user_model().objects.get(phone=request.user.phone)
            user.password = new_password
            user.save(update_fields=['password'])

            return Response({'message': 'Done!'}, status.HTTP_200_OK)

        else:
            raise SerializerException(serializer.errors)


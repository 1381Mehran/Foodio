from enum import Enum, unique

from django.db import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from product.models import Product
from .serializers import (
    ImprovePositionSerializer, ChangeAdminOrStaffPasswordSerializer, SellerSerializer, AcceptingSellerSerializer
)

from extensions.renderers import CustomJSONRenderer
from ..permissions import IsSuperUser, IsAdminOrStaff, IsProductAdmin
from ..models import Admin, Staff
from account.utils import Authentication
from extensions.api_exceptions import SerializerException
from seller.models import Seller


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


# Relating to Seller


class SellerListView(ListAPIView):
    serializer_class = SellerSerializer
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsProductAdmin | IsSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__phone', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        queryset = Seller.objects.all()
        status_ = self.request.query_params.get('status')

        @unique
        class Status(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        match status_:
            case Status.ACTIVE.value:
                queryset = queryset.filter(is_active=True)

            case Status.INACTIVE.value:
                queryset = queryset.filter(is_active=False)

        return queryset


class SellerAcceptanceView(APIView):
    permission_classes = [IsAuthenticated & IsProductAdmin]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = AcceptingSellerSerializer

    def put(self, request, pk, *args, **kwargs):
        try:
            instance = Seller.objects.get(id=pk)
        except Seller.DoesNotExist:
            return Response({'error': f'Seller with id {pk} does not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()

                if serializer.validated_data.get("is_active"):

                    password = Authentication().password_generator
                    instance.not_confirmed_cause = None
                    instance.user.password = password
                    instance.user.save(update_fields=['password'])
                    instance.save(update_fields=["not_confirmed_cause"])

                    return Response(
                        {
                            'phone': instance.user.phone,
                            'password': password
                        },
                        status=status.HTTP_200_OK
                    )

                else:
                    return Response({'Success': True})

            else:
                raise SerializerException(serializer.errors)







from enum import Enum, unique

from django.db import IntegrityError
from django.db.models import Value, CharField, Q
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, ListAPIView, get_object_or_404
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from foodio.celery import app as celery_app

from product.models import MainCat, MidCat, SubCat
from .serializers import (
    ImprovePositionSerializer, ChangeAdminOrStaffPasswordSerializer, SellerSerializer, AcceptingSellerSerializer,
    CategorySerializer
)
from extensions.renderers import CustomJSONRenderer
from ..permissions import IsSuperUser, IsAdminOrStaff, IsProductAdmin
from ..models import Admin, Staff
from account.utils import Authentication
from extensions.api_exceptions import SerializerException
from seller.models import Seller


class ImprovePositionView(ListCreateAPIView):
    serializer_class = ImprovePositionSerializer
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def list(self, request, *args, **kwargs):
        options = [Admin.AdminPosition.FINANCIAL, Admin.AdminPosition.TECHNICAL,
                   Admin.AdminPosition.PRODUCT, Admin.AdminPosition.SUPPORT]

        return Response({'options': options})

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

                if instance.celery_task_id:

                    task = celery_app.AsyncResult(instance.celery_task_id)
                    task.revoke(terminate=True)
                    instance.celery_task_id = None
                    instance.save(update_fields=['celery_task_id'])

                if serializer.validated_data.get("is_active"):

                    password = Authentication().password_generator
                    instance.not_confirmed_cause = None
                    instance.user.password = password
                    instance.user.save(update_fields=['password'])
                    instance.save(update_fields=["not_confirmed_cause", "celery_task_id"])

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


# relating to Products Part


class CatView(APIView):
    permission_classes = [IsAuthenticated & IsProductAdmin]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = CategorySerializer

    # todo : (Feature) add Search property base on title in Get Method

    def get(self, request, *args, **kwargs):

        type_ = self.request.query_params.get('type')
        search = self.request.query_params.get('search')

        class Type(Enum):
            ACTIVE = 'true', 'True'
            INACTIVE = 'false', 'False'

        if type_ == Type.ACTIVE.value[0]:
            type_ = Type.ACTIVE.value[1]

        elif type_ == Type.INACTIVE.value[0]:
            type_ = Type.INACTIVE.value[1]

        else:
            type_ = Type.INACTIVE.value[1]

        sub_cat = SubCat.objects.filter(is_active=type_)

        # separate duplicate Categories in Mid_cat and Main cat

        mid_cat = MidCat.objects.filter(~Q(id__in=sub_cat.values_list('parent_id')), is_active=type_)

        main_cats = MainCat.objects.filter(
            ~Q(id__in=sub_cat.values_list('parent__parent_id', flat=True)),
            ~Q(id__in=mid_cat.values_list('parent_id', flat=True)),
            is_active=type_
        ).only(
            'id', 'title', 'is_active'
        ).annotate(
            type=Value("main_cat", output_field=CharField()),
        )

        mid_cats = mid_cat.only(
            'id', 'title', 'is_active'
        ).annotate(type=Value("mid_cat", output_field=CharField()))

        sub_cats = sub_cat.only(
            'id', 'title', 'is_active'
        ).annotate(type=Value("sub_cat", output_field=CharField()))

        # combine all of QuerySets

        instances = main_cats.union(mid_cats, sub_cats)

        # Search Feature for title

        if search:
            instances = instances.annotate(
                similarity=TrigramSimilarity('title', search),
            ).filter(similarity__gte=0.3).order_by('-similarity')

        serializer = self.serializer_class(instance=instances, many=True)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            cat_type = serializer.validated_data.get('cat_type')
            instance = self.category_interface(cat_type, pk)

            if serializer.validated_data.get('active'):
                instance.is_active = serializer.validated_data.get('active')
                instance.save(update_fields=['is_active'])

            if serializer.validated_data.get('title'):
                instance.title = serializer.validated_data.get('title')
                instance.save(update_fields=['title'])

            return Response({'success': True}, status.HTTP_200_OK)
        else:
            raise SerializerException(serializer.errors)

    @classmethod
    def category_interface(cls, cat_type, pk):
        class Type(Enum):
            MAIN = 'main_cat'
            MID = 'mid_cat'
            SUB = 'sub_cat'

        match cat_type:
            case Type.MAIN.value:
                return get_object_or_404(MainCat, pk=pk)
            case Type.MID.value:
                return get_object_or_404(MidCat, pk=pk)
            case Type.SUB.value:
                return get_object_or_404(SubCat, pk=pk)





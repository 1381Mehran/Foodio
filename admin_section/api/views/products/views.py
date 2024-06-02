from enum import Enum

from django.db.models import Q, OuterRef, Exists
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from product.models import ProductCategory
from admin_section.api.serializers import (
    CategorySerializer, AdminAddEditCatSerializer
)

from extensions.renderers import CustomJSONRenderer
from admin_section.permissions import IsProductAdmin
from extensions.api_exceptions import SerializerException


class CatView(APIView):

    """
    get:
        get list of cats by type Parameters

        parameters :  [
                type(optional): type of categories {active categories or another},
                search(optional): Search based on categories title
        ]

    post:
        Create Categories by product Admins
        body : AddEditCatSerializer

    put:
        Update Categories by Product Admins

        body : CategorySerializer

    delete:
            delete a category by id

            body : [type(Required): this is required Option for find out type of category]

    category_interface : method for manage categories instance

    """

    permission_classes = [IsAuthenticated & IsProductAdmin]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = CategorySerializer
    post_serializer = AdminAddEditCatSerializer

    class Type(Enum):
        MAIN = 'main_cat'
        MID = 'mid_cat'
        SUB = 'sub_cat'

    @swagger_auto_schema(
        operation_summary="cat list",
        operation_description="get list of cats by type Parameters",
        manual_parameters=[
            openapi.Parameter(
                name='type',
                in_=openapi.IN_QUERY,
                description='type of categories',
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search based on categories title',
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response('success', CategorySerializer)
        }

    )
    @action(detail=True, methods=['GET'])
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

        excludes = ProductCategory.objects.filter(
            parent=OuterRef('pk'),
            is_active=type_,
        )

        query_set = ProductCategory.objects.filter(
            Q(is_active=type_) | Q(parent__is_active=type_) | Q(parent__parent__is_active=type_)
        ).exclude(Exists(excludes))

        if type_ == 'True':
            query_set = query_set.filter(
                Q(
                    Q(parent__isnull=True) &
                    ~Q(is_active=False)
                ) |
                Q(
                    Q(parent__isnull=False) &
                    Q(parent__parent__isnull=True) &
                    ~Q(is_active=False) &
                    ~Q(parent__is_active=False)
                ) |
                Q(
                    Q(parent__parent__isnull=False) &
                    ~Q(is_active=False) &
                    ~Q(parent__is_active=False) &
                    ~Q(parent__parent__is_active=False)
                )
            )

        if search:
            query_set = query_set.annotate(
                title_similarity=TrigramSimilarity('title', search),
                parent_title_similarity=TrigramSimilarity('parent__title', search),
                parent_parent_title_similarity=TrigramSimilarity('parent__parent__title', search),

            ).annotate(
                hightest_similarity=Greatest(
                    'title_similarity',
                    'parent_title_similarity',
                    'parent_parent_title_similarity'
                )
            ).filter(hightest_similarity__gte=0.2)

        serializer = self.serializer_class(instance=query_set, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="cat add",
        operation_description="Add Category by Product Admin",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='id of cat',
                required=False
            )
        ],
        request_body=AdminAddEditCatSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('success', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.post_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})

        else:
            raise SerializerException(serializer.errors)

    @swagger_auto_schema(
        operation_summary="cat Update",
        operation_description="update Categories by Product Admins",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='id of cat',
                required=True
            )
        ],
        request_body=serializer_class,
        responses={
            status.HTTP_200_OK: openapi.Response('success', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )),
            status.HTTP_404_NOT_FOUND: openapi.Response("Not Found", openapi.Schema(type=openapi.TYPE_STRING)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('invalid input')
        }
    )
    @action(detail=True, methods=['PUT'])
    def put(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(ProductCategory, pk=pk)

        serializer = self.post_serializer(data=request.data, instance=instance, partial=True)

        if serializer.is_valid():

            # if serializer.validated_data.get('active'):
            #     instance.is_active = serializer.validated_data.get('active')
            #     instance.save(update_fields=['is_active'])
            #
            # if serializer.validated_data.get('title'):
            #     instance.title = serializer.validated_data.get('title')
            #     instance.save(update_fields=['title'])

            serializer.save()

            return Response({'success': True}, status.HTTP_200_OK)
        else:
            raise SerializerException(serializer.errors)

    @swagger_auto_schema(
        operation_summary="cat Delete",
        operation_description="Delete Categories by Product Admins",
        manual_parameters=[
           openapi.Parameter(
               'id',
               in_=openapi.IN_QUERY,
               type=openapi.TYPE_STRING,
               required=False,
               description='dont\'t need to fill this field'
            ),

        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
            },
            description="type of category"
        ),
        responses={
            status.HTTP_200_OK: openapi.Response('success', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )),
            status.HTTP_404_NOT_FOUND: openapi.Response("Not Found", openapi.Schema(type=openapi.TYPE_STRING)),
        }
    )
    def delete(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(ProductCategory, pk=pk)

        instance.delete()

        return Response({'success': True}, status.HTTP_204_NO_CONTENT)

    # @classmethod
    # def category_interface(cls, cat_type, pk):
    #
    #     match cat_type:
    #         case cls.Type.MAIN.value:
    #             return get_object_or_404(MainCat, pk=pk)
    #         case cls.Type.MID.value:
    #             return get_object_or_404(MidCat, pk=pk)
    #         case cls.Type.SUB.value:
    #             return get_object_or_404(SubCat, pk=pk)

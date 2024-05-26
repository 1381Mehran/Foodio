from enum import Enum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from extensions.renderers import CustomJSONRenderer
from extensions.api_exceptions import SerializerException

from ...serializers import (ProductSerializer, ProductImagesSerializer, ProductPropertySerializer)

from product.models import Product, ProductImage, ProductProperty
from seller.permissions import IsSellerProduct


class ProductView(APIView):

    """
    get :
        List or Retrieve all products that relating to specific seller

        query_parameters = [type(optional): seller product type]


    """

    class ProductType(Enum):
        PUBLISHED = 'published'
        PENDING = 'pending'
        DRAFT = 'draft'
        NOT_CONFIRMED = 'not_confirmed'

    renderer_classes = [CustomJSONRenderer]
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary='Seller Product',
        operation_description='get or retrieve all sellers products',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='product_id',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response('Success', ProductSerializer),
            "200-retrieve": openapi.Response('Success', serializer_class),
            "404": openapi.Response('Product not found'),
            '400': openapi.Response('Bad Request')
        }

    )
    def get(self, request, pk=None):
        if pk:
            try:
                instance = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                raise NotFound(f'Product with id {pk} does not exist')

            else:
                serializer = self.serializer_class(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:

            type_ = self.request.query_params.get('type', None)
            queryset = request.user.products.all()

            match type_:
                case self.ProductType.PUBLISHED.value:
                    queryset = queryset.filter(product_type=self.ProductType.PUBLISHED.value)

                case self.ProductType.PENDING.value:
                    queryset = queryset.filter(product_type=self.ProductType.PENDING.value)

                case self.ProductType.DRAFT.value:
                    queryset = queryset.filter(product_type=self.ProductType.DRAFT.value)

                case self.ProductType.NOT_CONFIRMED.value:
                    queryset = queryset.filter(product_type=self.ProductType.NOT_CONFIRMED.value)

                case _:
                    queryset = queryset.filter(product_type=self.ProductType.DRAFT.value)

            serializer = self.serializer_class(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Seller Product',
        operation_description='add sellers products',
        request_body=ProductSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Success',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['seller'] = request.user
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            raise SerializerException(serializer.errors)

    @swagger_auto_schema(
        operation_summary='modify seller product',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='product_id',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=ProductSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response("success", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_STRING)),
            status.HTTP_400_BAD_REQUEST: "Problem in serializer"
        }

    )
    def put(self, request, pk):
        try:
            instance = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise NotFound(f'Product with id {pk} does not exist')

        else:
            self.check_object_permissions(request, instance)

            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.update({'is_active': False})
                serializer.validated_data.update({'product_type': 'draft'})
                serializer.save()

                return Response({'success': True}, status.HTTP_202_ACCEPTED)

            else:
                raise SerializerException(serializer.errors)

    @swagger_auto_schema(
        operation_summary='delete sellers product',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='product_id',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response('Success', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_STRING)),
        }
    )
    def delete(self, request, pk):
        try:
            instance = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise NotFound(f'Product with id {pk} does not exist')
        else:

            self.check_object_permissions(request, instance)

            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsSellerProduct]

        super(ProductView, self).get_permissions()


class ProductImageView(APIView):
    permission_classes = [IsAuthenticated & IsSellerProduct]
    serializer_class = ProductImagesSerializer

    def get_object(self, request, pk):
        instance = get_object_or_404(ProductImage, pk=pk, product__seller__user=request.user)
        self.check_object_permissions(request, instance)

        return instance

    def put(self, request, pk, *args, **kwargs):

        instance = self.get_object(request, pk)

        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            instance.product.is_active = False
            instance.product.product_type = 'draft'
            instance.product.save(update_fields=['is_active', 'product_type'])

            return Response({'success': True}, status.HTTP_202_ACCEPTED)

        else:
            raise SerializerException(serializer.errors)

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(request, pk)

        instance.product.is_active = False
        instance.product.product_type = 'draft'
        instance.product.save(update_fields=['is_active', 'product_type'])

        instance.delete()

        return Response({'success': True}, status.HTTP_204_NO_CONTENT)


class ProductPropertyView(APIView):
    permission_classes = [IsAuthenticated & IsSellerProduct]
    serializer_class = ProductPropertySerializer

    def get_object(self, request, pk):
        instance = get_object_or_404(ProductProperty, pk=pk, product__seller__user=request.user)
        self.check_object_permissions(request, instance)
        return instance

    def put(self, request, pk, *args, **kwargs):
        instance = self.get_object(request, pk)

        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            instance.product.is_active = False
            instance.product.product_type = 'draft'
            instance.product.save(update_fields=['is_active', 'product_type'])

            return Response({'success': True}, status.HTTP_202_ACCEPTED)

        else:
            raise SerializerException(serializer.errors)

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(request, pk)

        instance.product.is_active = False
        instance.product.product_type = 'draft'
        instance.product.save(update_fields=['is_active', 'product_type'])

        instance.delete()

        return Response({'success': True}, status.HTTP_204_NO_CONTENT)

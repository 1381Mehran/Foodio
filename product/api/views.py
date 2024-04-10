from enum import Enum, unique

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from seller.permissions import IsSeller
from ..permissions import IsCatAdminOrReadOnly, IsSellerProduct
from .serializers import (GetCatSerializer, AddEditCatSerializer, ProductSerializer, RetrieveProductSerializer)
from extensions.api_exceptions import SerializerException
from extensions.renderers import CustomJSONRenderer
from ..models import MainCat, MidCat, SubCat, Product
from extensions.loggers import logger_error


class CatView(APIView):
    permission_classes = [IsAuthenticated & IsCatAdminOrReadOnly]
    renderer_classes = [CustomJSONRenderer]

    def detect_cat(self, type_, pk):

        @unique
        class CatType(Enum):
            MAIN_CAT = 'main_cat'
            MID_CAT = 'mid_cat'
            SUB_CAT = 'sub_cat'

        instance = None

        match type_:
            case CatType.MAIN_CAT.value:
                try:
                    instance = MainCat.objects.get(id=pk)
                except MainCat.DoesNotExist:
                    return Response({'error': f'Main Cat with id {pk} does not exist'}, status=404)

            case CatType.MID_CAT.value:
                try:
                    instance = MidCat.objects.get(id=pk)
                except MidCat.DoesNotExist:
                    return Response({'error': f'Mid Cat with id {pk} does not exist'}, status=404)

            case CatType.SUB_CAT.value:
                try:
                    instance = SubCat.objects.get(id=pk)
                except SubCat.DoesNotExist:
                    return Response({'error': f'Mid Cat with id {pk} does not exist'}, status=404)

        return instance

    def get(self, request, pk=None):
        if pk:
            type_ = request.query_params.get('type', None)

            if type_:
                instance = self.detect_cat(type_, pk)

                if isinstance(instance, str):
                    return Response({'error': instance}, status=404)
                else:
                    serializer = GetCatSerializer(instance, context={'type': type_})
                    return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Type is required'}, status=400)

        else:
            main_cats = MainCat.objects.filter(active=True).only('id', 'title')
            mid_cats = MidCat.objects.filter(active=True).only('id', 'title')
            sub_cats = SubCat.objects.filter(active=True).only('id', 'title')

            data = {
                'main_cats': [{"id": _.id, "title": _.title} for _ in main_cats],
                'mid_cats': [
                    {"id": _.id, "title": _.title, 'main_cat_id': {'id':  _.parent.id, 'title': _.parent.title}}
                    for _ in mid_cats
                ],

                'sub_cats': [
                    {"id": _.id, "title": _.title, 'mid_cat_id': {'id': _.parent.id, 'title': _.parent.title}}
                    for _ in sub_cats
                ]
            }

            return Response(data)

    def post(self, request, format=None):
        serializer = AddEditCatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            raise SerializerException(serializer.errors)

    def put(self, request, pk, format=None):
        serializer = AddEditCatSerializer(data=request.data)
        if serializer.is_valid():
            type_ = serializer.data.get('type')
            title = serializer.data.get('title', None)
            parent_id = serializer.data.get('parent_id', None)

            instance = self.detect_cat(type_, pk)

            if isinstance(instance, str):
                return Response({'error': instance}, status=404)
            else:
                if title:
                    instance.title = serializer.data.get('title')
                if parent_id:
                    instance.parent_id = serializer.data.get('parent_id')
                    instance.save(update_fields=['parent_id'])

                return Response({'success': True}, status.HTTP_202_ACCEPTED)

        else:
            raise SerializerException(serializer.errors)

    def delete(self, request, pk):
        type_ = self.request.query_params.get('type', None)

        if type_:
            instance = self.detect_cat(type_, pk)
            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': 'Type is required'}, status=400)


class SellerProductView(APIView):
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
            "200-retrieve": openapi.Response('Success', RetrieveProductSerializer),
            "404": openapi.Response('Product not found'),
            '400': openapi.Response('Bad Request')
        }

    )
    def get(self, request, pk=None):
        if pk:
            try:
                instance = Product.objects.get(pk=pk)
            except Product.DoesNotExist:

                return Response({'error': f'Product with id {pk} does not exist'}, status=404)
            else:
                serializer = RetrieveProductSerializer(instance, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            serializer = self.serializer_class(instance=request.user.products.all(), many=True)
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
            serializer.validated_data['user'] = request.user
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
            return Response({'error': f'Product with id {pk} does not exist'}, status=404)

        else:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
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
            return Response({'error': f'Product with id {pk} does not exist'}, status=404)
        else:
            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsSeller, IsSellerProduct]

        super(SellerProductView, self).get_permissions()
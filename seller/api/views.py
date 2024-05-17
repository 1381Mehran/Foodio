from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import State, Seller
from admin_section.permissions import IsSupportAdmin, IsTechnicalAdmin, IsSuperUser
from .serializers import (RetrieveStateSerializer, CreateAndUpdateStateSerializer, SellerSerializer, ProductSerializer,
                          RetrieveProductSerializer)
from extensions.api_exceptions import SerializerException
from extensions.renderers import CustomJSONRenderer
from ..permissions import IsSeller, IsSellerProduct
from product.models import Product


class StateView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def get(self, request, pk=None, *args, **kwargs):

        if pk:
            instance = get_object_or_404(State, pk=pk, is_active=True)
            serializer = RetrieveStateSerializer(instance=instance)
            return Response(serializer.data)
        else:
            instances = State.objects.filter(is_active=True, type='state', parent__isnull=True)
            serializer = RetrieveStateSerializer(instance=instances, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CreateAndUpdateStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'Success': True}, status=201)

        else:
            raise SerializerException(serializer.errors)

    def put(self, request, pk, *args, **kwargs):
        # instance = get_object_or_404(State, pk=pk)
        try:
            instance = State.objects.get(pk=pk)
        except State.DoesNotExist:
            return Response({'error': 'State/city not found'}, status=404)
        else:
            serializer = CreateAndUpdateStateSerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': True}, status.HTTP_202_ACCEPTED)
            else:
                raise SerializerException(serializer.errors)

    def delete(self, request, pk, *args, **kwargs):
        # instance = get_object_or_404(State, pk=pk)
        try:
            instance = State.objects.get(pk=pk)
        except State.DoesNotExist:
            return Response({'error': 'State/city not found'}, status=404)
        else:
            instance.delete()
            return Response({'Success': True}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsSuperUser | IsSupportAdmin | IsTechnicalAdmin]

        return super(StateView, self).get_permissions()


class SellerView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)

        if serializer.is_valid():
            if (request.user.first_name and request.user.last_name and request.user.national_id and
                    (request.user.card_numbers.filter(is_active=True).count() > 0)):
                serializer.validated_data['user'] = request.user
                serializer.save()
                return Response({'success': True}, status.HTTP_201_CREATED)

            else:
                return Response(
                    {'error': 'first name , last name and national id are required and you have to have at least one card number'},
                    status.HTTP_406_NOT_ACCEPTABLE
                )

        else:
            raise SerializerException(serializer.errors)

    def put(self, request, pk, *args, **kwargs):
        try:
            instance = Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            return Response({'error': f'Seller with id {pk} not found'}, status=404)

        else:
            serializer = SellerSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True}, status.HTTP_202_ACCEPTED)

            else:
                raise SerializerException(serializer.errors)

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            return Response({'error': f'Seller with id {pk} not found'}, status=404)

        else:
            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsSeller]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(SellerView,self).get_permissions()


class ProductView(APIView):
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
            raise NotFound(f'Product with id {pk} does not exist')

        else:
            self.check_object_permissions(request, instance)

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
            raise NotFound(f'Product with id {pk} does not exist')
        else:

            self.check_object_permissions(request, instance)

            instance.delete()
            return Response({'success': True}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsSeller, IsSellerProduct]

        super(ProductView, self).get_permissions()

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.generics import get_object_or_404

from ..models import State, Seller
from admin_section.permissions import IsSupportAdmin, IsTechnicalAdmin
from .serializers import RetrieveStateSerializer, CreateAndUpdateStateSerializer, SellerSerializer
from extensions.api_exceptions import SerializerException
from extensions.renderers import CustomJSONRenderer
from ..permissions import IsSeller


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
            self.permission_classes = [IsSupportAdmin | IsTechnicalAdmin]

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


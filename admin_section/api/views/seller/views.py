from enum import Enum, unique

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from foodio.celery import app as celery_app

from admin_section.api.serializers import (
    SellerSerializer, AcceptingSellerSerializer
)

from extensions.renderers import CustomJSONRenderer
from extensions.send_mail import SendMailThread
from admin_section.permissions import IsSuperUser, IsProductAdmin
from account.utils import Authentication
from extensions.api_exceptions import SerializerException
from seller.models import Seller


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
            raise NotFound(f'Seller with id {pk} does not found.')

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

                    SendMailThread(
                        'شرکت جاوید',
                        f" نام کاربری : {instance.user.phone} \n {password}رمز عبور : ",
                        [instance.user.email],
                    ).start()

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

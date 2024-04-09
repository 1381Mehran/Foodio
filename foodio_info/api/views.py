from enum import Enum

from django.utils import timezone
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework .response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_swagger.views import get_swagger_view

from extensions.renderers import CustomJSONRenderer
from admin_section.permissions import IsSuperUser


schema_view = get_swagger_view(title='Foodio INFO API')


class ServerTimeView(APIView):
    renderer_classes = [CustomJSONRenderer]

    @swagger_auto_schema(
        operation_summary='Server time',
        operation_description='get exactly the server time',
        responses={
            200: openapi.Response(
                description='return server time',
                examples={
                    'application/json': [
                        '"server_time": "2024-04-05 01:11:33.795150+03:30"'
                    ],
                },
            ),
            '500': 'Internal Server Error',
        },
    )
    def get(self, request):

        return Response(
            {'server_time': str(timezone.localtime(timezone.now()))}
        )


class LogsView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated & IsSuperUser]

    @swagger_auto_schema(
        operation_summary='Error logs',
        responses={
            status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_STRING)
        },
        security=[{'Bearer': []}]
    )
    def get(self, request):
        level = request.query_params.get('level', None)

        class Levels(Enum):
            INFO = 'info'
            ERROR = 'error'

        match level:
            case Levels.ERROR.value:
                with open(f'{settings.BASE_DIR}/logs/ERROR.log', 'r') as f:
                    return Response({'logs': f.readlines()[-30:]})

            case Levels.INFO.value:
                with open(f'{settings.BASE_DIR}/logs/INFO.log', 'r') as f:
                    return Response({'logs': f.readlines()[-30:]})

            case _:
                return Response({'error': 'Invalid level'})


class CeleryWorkerLogsView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated & IsSuperUser]

    @swagger_auto_schema(
        operation_summary='Error logs',
        responses={
            status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_STRING)
        },
        security=[{'Bearer': []}]
    )
    def get(self, request):
        with open(f'{settings.BASE_DIR}/logs/CELERY_WORKER.log', 'r') as f:
            return Response({'logs': f.readlines()[50:]})

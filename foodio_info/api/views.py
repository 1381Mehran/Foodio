from django.utils import timezone

from rest_framework .response import Response
from rest_framework.views import APIView

from extensions.renderers import CustomJSONRenderer


class ServerTimeView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        return Response(
            {'server_time': str(timezone.localtime(timezone.now()))}
        )


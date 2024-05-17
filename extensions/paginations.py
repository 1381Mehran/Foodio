from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = int(settings.PAGE_SIZE)
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'metadata': {
                'total_items': self.page.paginator.count,
                'current_page': self.page.number,
                'last_page':  self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request),
            },
            'data': data
        })

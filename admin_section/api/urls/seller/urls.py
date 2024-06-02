from django.urls import re_path
from admin_section.api.views import (SellerListView, SellerAcceptanceView)

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'^seller-list/?$', SellerListView.as_view(), name=''),
    re_path(r'^accept-seller/(?P<pk>[-\d]+)/?$', SellerAcceptanceView.as_view(), name='accept-seller'),
]



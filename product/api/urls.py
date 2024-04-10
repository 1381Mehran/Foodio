from django.urls import re_path
from .views import (CatView, SellerProductView)

app_name = 'product'


urlpatterns = [
    re_path(r'^cat/(?P<pk>[-\d])?/?$', CatView.as_view(), name='cat-view'),
    re_path(r'^product/(?P<pk>[-\d])?/?$', SellerProductView.as_view(), name='seller-product'),
]

from django.urls import re_path
from .views import StateView, SellerView, ProductView

app_name = 'seller'

urlpatterns = [
    re_path(r'^(?P<pk>[-\d]+)?/?$', SellerView.as_view(), name='seller'),
    re_path(r'^state/(?P<pk>[-\d]+)?/?$', StateView.as_view(), name='state'),
    re_path(r'^product/(?P<pk>[-\d])?/?$', ProductView.as_view(), name='seller-product'),
]


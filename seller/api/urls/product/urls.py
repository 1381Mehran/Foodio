from django.urls import re_path
from ...views import ProductView, ProductPropertyView, ProductImageView


urlpatterns = [
    re_path(r'^product/(?P<pk>[-\d])?/?$', ProductView.as_view(), name='seller-product'),
    re_path(
        r'^product/(?P<p_pk>[-\d])/property/(?P<pk>[-\d])/?$',
        ProductPropertyView.as_view(),
        name='seller-product'
    ),
    re_path(r'^product/(?P<p_pk>[-\d])/image/(?P<pk>[-\d])/?$', ProductImageView.as_view(), name='seller-product'),
]
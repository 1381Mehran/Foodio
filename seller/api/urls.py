from django.urls import re_path
from .views import (
    StateView, SellerView, ProductView, ChangeSellerPasswordView, ProductPropertyView, ProductImageView
)

app_name = 'seller'

urlpatterns = [

    ##############################################################
    #                       Seller Views                        #
    ##############################################################

    re_path(r'^(?P<pk>[-\d]+)?/?$', SellerView.as_view(), name='seller'),
    re_path(r'^password/?$', ChangeSellerPasswordView.as_view(), name='change-seller-password'),
    re_path(r'^state/(?P<pk>[-\d]+)?/?$', StateView.as_view(), name='state'),

    ##############################################################
    #                       Product Views                        #
    ##############################################################

    re_path(r'^product/(?P<pk>[-\d])?/?$', ProductView.as_view(), name='seller-product'),
    re_path(
        r'^product/(?P<p_pk>[-\d])/property/(?P<pk>[-\d])/?$',
        ProductPropertyView.as_view(),
        name='seller-product'
    ),
    re_path(r'^product/(?P<p_pk>[-\d])/image/(?P<pk>[-\d])/?$', ProductImageView.as_view(), name='seller-product'),
]


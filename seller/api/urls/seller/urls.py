from django.urls import re_path
from ...views import SellerView, ChangeSellerPasswordView, StateView


urlpatterns = [
    re_path(r'^(?P<pk>[-\d]+)?/?$', SellerView.as_view(), name='seller'),
    re_path(r'^password/?$', ChangeSellerPasswordView.as_view(), name='change-seller-password'),
    re_path(r'^state/(?P<pk>[-\d]+)?/?$', StateView.as_view(), name='state'),
]
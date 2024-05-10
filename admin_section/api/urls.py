from django.urls import re_path
from .views import (ImprovePositionView, ChangeAdminOrStaffPasswordView, SellerListView, SellerAcceptanceView,
                    CatView)

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'^improve-user/?$', ImprovePositionView.as_view(), name='improve_user'),
    re_path(r'^change-password/?$', ChangeAdminOrStaffPasswordView.as_view(), name='change_password'),

    # relating to Seller Part

    re_path(r'^seller-list/?$', SellerListView.as_view(), name=''),
    re_path(r'^accept-seller/(?P<pk>[-\d]+)/?$', SellerAcceptanceView.as_view(), name='accept-seller'),

    # relating to Products

    re_path(r'cat/(?P<pk>[-\d]+)?/?$', CatView.as_view(), name='admin-cat'),

]


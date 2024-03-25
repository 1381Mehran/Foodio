from django.urls import re_path
from .views import (ImprovePositionView, ChangeAdminOrStaffPasswordView, SellerListView)

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'^improve-user/?$', ImprovePositionView.as_view(), name='improve_user'),
    re_path(r'^change-password/?$', ChangeAdminOrStaffPasswordView.as_view(), name='change_password'),
    re_path(r'^seller-list/?$', SellerListView.as_view(), name='')
]


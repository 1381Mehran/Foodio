from django.urls import re_path
from admin_section.api.views import (ImprovePositionView, ChangeAdminOrStaffPasswordView)

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'^improve-user/?$', ImprovePositionView.as_view(), name='improve_user'),
    re_path(r'^change-password/?$', ChangeAdminOrStaffPasswordView.as_view(), name='change_password'),
]


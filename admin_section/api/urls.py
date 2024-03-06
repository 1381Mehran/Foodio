from django.urls import re_path
from .views import *

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'^improve-user/?$', ImprovePositionView.as_view(), name='improve_user'),
]


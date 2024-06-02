from django.urls import re_path
from admin_section.api.views import (CatView)

app_name = 'api_admin_section'

urlpatterns = [
    re_path(r'cat/(?P<pk>[-\d]+)?/?$', CatView.as_view(), name='admin-cat'),
]

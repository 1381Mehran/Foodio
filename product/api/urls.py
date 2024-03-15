from django.urls import re_path
from .views import (CatView)

app_name = 'product'


urlpatterns = [
    re_path(r'^cat/(?P<pk>[-\d])?/?$', CatView.as_view(), name='cat-view'),
]

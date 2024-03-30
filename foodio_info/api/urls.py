from django.urls import re_path
from . import views


app_name = 'info'

urlpatterns = [
    re_path(r'^time/?$', views.ServerTimeView.as_view(), name='ServerTime'),
]
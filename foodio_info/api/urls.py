from django.urls import re_path
from . import views


app_name = 'info'

urlpatterns = [
    re_path(r'^time/?$', views.ServerTimeView.as_view(), name='ServerTime'),

    # Logs routes

    re_path(r'^log/?$', views.LogsView.as_view(), name='ErrorLogs'),
    re_path(r'^log-celery/?$', views.CeleryWorkerLogsView.as_view(), name='CeleryWorkerLogs'),
]
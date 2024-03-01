from django.urls import re_path

from .views import LoginView

app_name = 'api_account'

urlpatterns = [
    re_path(r'^login/?$', LoginView.as_view(), name='api_login')
]
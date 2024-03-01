from django.urls import re_path

from .views import LoginView, VerifyView, LogoutView

app_name = 'api_account'

urlpatterns = [
    re_path(r'^login/?$', LoginView.as_view(), name='api_login'),
    re_path(r"^verify/?$", VerifyView.as_view(), name='api_verify'),
    re_path(r'^logout/?$', LogoutView.as_view(), name='api_logout'),
]
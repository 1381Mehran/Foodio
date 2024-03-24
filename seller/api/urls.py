from django.urls import re_path
from .views import StateView

app_name = 'seller'

urlpatterns = [
    re_path(r'^state/(?P<pk>[-\d])?/?$', StateView.as_view(), name='state'),
]


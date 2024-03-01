from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Api

    path('api/v1/account/', include('account.api.urls')),
]

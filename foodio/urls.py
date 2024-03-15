from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Api

    path('api/v1/account/', include('account.api.urls')),
    path('api/v1/admin-section/', include('admin_section.api.urls')),
    path('api/v1/product/', include('product.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
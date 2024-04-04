from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Api

    path('api/v1/account/', include('account.api.urls')),
    path('api/v1/admin-section/', include('admin_section.api.urls')),
    path('api/v1/product/', include('product.api.urls')),
    path('api/v1/seller/', include('seller.api.urls')),
    path('api/v1/info/', include('foodio_info.api.urls')),


    # Relating to Swagger

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
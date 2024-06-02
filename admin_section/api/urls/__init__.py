from .admin_section.urls import urlpatterns as admin_section_urls
from .products.urls import urlpatterns as products_urls
from .seller.urls import urlpatterns as sellers_urls

app_name = 'api_admin_section'

urlpatterns = [
    *admin_section_urls,
    *products_urls,
    *sellers_urls,
]


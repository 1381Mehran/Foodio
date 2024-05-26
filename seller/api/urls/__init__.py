from .seller.urls import urlpatterns as seller_patterns
from .product.urls import urlpatterns as product_patterns


urlpatterns = []

urlpatterns += seller_patterns
urlpatterns += product_patterns

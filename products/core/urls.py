from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/category/', include('apps.category.urls')),
    path('api/products/', include('apps.product.urls')),
    path('api/shipping/', include('apps.shipping.urls')),
    path('admin/', admin.site.urls),
]

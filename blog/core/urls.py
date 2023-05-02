from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/posts/', include('apps.posts.urls')),
    path('api/category/', include('apps.category.urls')),
    path('admin/', admin.site.urls),
]

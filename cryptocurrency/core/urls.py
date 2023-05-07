from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/tokens/', include('apps.tokens.urls')),
    path('admin/', admin.site.urls),
]

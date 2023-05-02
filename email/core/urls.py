from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('api/contacts/', include('apps.contacts.urls')),
    path('admin/', admin.site.urls),
]

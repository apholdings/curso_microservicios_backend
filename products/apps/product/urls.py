from django.urls import path

from .views import *

urlpatterns = [
    path('list/', SearchProductsView.as_view())
]

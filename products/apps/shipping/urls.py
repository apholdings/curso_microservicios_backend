from django.urls import path
from .views import *

urlpatterns = [
    path('get-shipping-options', ListShippingOptionsView.as_view()),
    path('get/<id>/', GetShippingView.as_view()),
    path("create/",UpdateShippingView.as_view()),
    path("delete/",DeleteShippingView.as_view()),
]
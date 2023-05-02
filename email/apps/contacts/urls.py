from django.urls import path
from .views import *


urlpatterns = [
    path('', ContactCreateView.as_view()),
]

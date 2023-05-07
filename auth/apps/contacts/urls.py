from django.urls import path
from .views import *

urlpatterns = [
    path('my_contact_lists/', GetMyContactListsView.as_view(), name='my_contact_lists'),

]
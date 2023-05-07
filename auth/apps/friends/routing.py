from django.urls import re_path

from .consumers import FriendsConsumer

websocket_urlpatterns = [
    re_path(r'ws/friends/$', FriendsConsumer.as_asgi()),
]
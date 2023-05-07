from django.urls import re_path

from .consumer import SendTokensConsumer

websocket_urlpatterns = [
    re_path(r'^ws/send_tokens/(?P<room_name>[^/]+)/$', SendTokensConsumer.as_asgi()),
]
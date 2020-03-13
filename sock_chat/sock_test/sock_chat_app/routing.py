from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sock_chat_app/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
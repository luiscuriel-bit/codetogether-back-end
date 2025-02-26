from django.urls import re_path

from .consumers import CodeConsumer

websocket_urlpatterns = [
    re_path(r"ws/code/(?P<project>[\w-]+)/$", CodeConsumer.as_asgi()),
]

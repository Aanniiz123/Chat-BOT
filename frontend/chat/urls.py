from django.urls import path
from .views import create_conversation, get_conservation, home, index

urlpatterns = [
    path("", home, name="home"),
    path("index/", index, name="index"),
    path("create_conversation/", create_conversation, name="create_conversation"),
    path("get_conservation/", get_conservation, name="get_conservation"),
]

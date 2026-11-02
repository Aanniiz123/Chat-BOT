from django.urls import path
from .views import create_conversation, delete_conversation, get_conservation, home, index

urlpatterns = [
    path("", home, name="home"),
    path("index/", index, name="index"),
    path("create_conversation/", create_conversation, name="create_conversation"),
    path("get_conservation/", get_conservation, name="get_conservation"),
    path("delete_conversation/<int:conversation_id>/", delete_conversation, name="delete_conversation"),
]

from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("chat/private/<str:username>/", views.private_chat, name="private_chat"),
]
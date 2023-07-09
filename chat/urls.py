from django.urls import path

from . import views


urlpatterns = [
    # path("room_name/", views.CustomChat.as_view()),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
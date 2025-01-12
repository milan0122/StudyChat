from django.urls import path
from . import views

#list of urlpattern and this for only specific app
urlpatterns = [
    path("",views.home, name="home"),
    path("room/<str:id>/",view=views.room,name="room"),
    path("create-room/",view=views.create_room,name="create-room"),
    path("update-room/<str:id>",view=views.updateRoom, name="update-room")
]
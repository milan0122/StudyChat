from django.urls import path
from . import views

#list of urlpattern and this for only specific app
urlpatterns = [
    path("",views.home, name="home"),
    path("room/",view=views.room,name="room")
]
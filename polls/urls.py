from django.urls import path
from . import views

#list of urlpattern and this for only specific app
urlpatterns = [
    path('login/',view=views.loginPage,name="login"),
    path('logout/',view=views.logoutUser,name="logout"),
    path('register/',view=views.registerUser,name="register"),
    path("",views.home, name="home"),
    path("room/<str:id>/",view=views.room,name="room"),
     path("profile/<str:id>/",view=views.userProfile,name="user-profile"),
    path("create-room/",view=views.create_room,name="create-room"),
    path("update-room/<str:id>/",view=views.updateRoom, name="update-room"),
    path("delete-room/<str:id>/",view=views.deleteRoom, name="delete-room"),
    path("delete-message/<str:id>/",view=views.deleteMessage, name="delete-message")

]
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.createroom,name="createroom"),
    path('update-room/<str:pk>/',views.updateroom,name="updateroom"),
    path('login/',views.Loginpage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    
    path('delete-room/<str:pk>/',views.delete,name="deleteroom"),
    path('delete-message/<str:pk>/',views.deletemessage,name="deletemessage"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),
]
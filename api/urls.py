from django.urls import path
from . import views

urlpatterns = [
    path('room', views.RoomView.as_view()),
    path('create-room', views.CreateRoomView.as_view()),
    path('get-room', views.GetRoom.as_view()),
    path('join-room', views.JoinRoom.as_view()),
    path('user-in-room', views.UserInRoom.as_view()),
    # path('api/endpoint1/', views.endpoint1_view, name='endpoint1'),
    # path('api/endpoint2/', views.endpoint2_view, name='endpoint2'),
    # Add more paths for your API endpoints here
]

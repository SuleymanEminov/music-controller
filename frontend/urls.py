from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name=''),
    path('info', views.index, name='info'),
    path('join', views.index, name='join'),
    path('create', views.index, name='create'),
    path('room/<str:roomCode>', views.index, name='room')
]
